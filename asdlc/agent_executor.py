import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from .llm_client import call_llm
from .utils import find_project_root, detect_test_framework, console

logger = logging.getLogger(__name__)

class AgentHarness:
    """
    O 'Harness' é o ambiente operacional do agente.
    Ele empacota instruções, contexto do repositório e ferramentas de validação.
    """
    def __init__(self, agent_type: str, story_id: str, project_root: Path):
        self.agent_type = agent_type
        self.story_id = story_id
        self.project_root = project_root
        self.harness_dir = project_root / ".asdlc" / "harness" / f"{story_id}_{agent_type}"
        self.harness_dir.mkdir(parents=True, exist_ok=True)

    def prepare_context(self, task_description: str, relevant_files: List[str]) -> str:
        """
        Prepara um contexto enxuto (lean context) para o agente.
        Evita o inchaço de abstração (Abstraction Bloat) e economiza tokens.
        """
        # 1. Carregar Persona
        persona_path = self.project_root / ".asdlc" / "agents" / f"{self.agent_type}_agent.md"
        persona = persona_path.read_text(encoding="utf-8") if persona_path.exists() else f"Você é um agente do tipo {self.agent_type}."

        # 2. Carregar PROJECT_CONTEXT.md (apenas os primeiros 3000 caracteres para evitar 429)
        project_context_path = self.project_root / "PROJECT_CONTEXT.md"
        lean_context = ""
        if project_context_path.exists():
            full_context = project_context_path.read_text(encoding="utf-8")
            lean_context = full_context[:3000] + "\n[Conteúdo truncado para economizar tokens...]" if len(full_context) > 3000 else full_context
        
        # 3. Carregar conteúdo dos arquivos relevantes (com limite de tamanho por arquivo)
        files_content = ""
        for file_rel_path in relevant_files:
            file_path = self.project_root / file_rel_path
            if file_path.exists() and file_path.is_file():
                # Limite de 5000 chars por arquivo para proteção
                content = file_path.read_text(encoding="utf-8")
                if len(content) > 5000:
                    content = content[:5000] + "\n[... Arquivo muito grande, truncado ...]"
                files_content += f"\n--- ARQUIVO: {file_rel_path} ---\n{content}\n"

        # 4. Montar o prompt final
        prompt = f"""
{persona}

## 🌐 CONTEXTO DO PROJETO (LEAN)
{lean_context}

## 📂 ARQUIVOS RELEVANTES
{files_content}

## 🛠️ FERRAMENTAS DISPONÍVEIS
Você pode delegar subtarefas para outros especialistas se necessário.
Para delegar, use o formato: [DELEGATE: tipo_do_agente | descrição_da_subtarefa]
Tipos disponíveis: code, test, architecture, requirements, review, bug_hunter.

## 🎯 SUA TAREFA ATUAL
{task_description}

## 📋 DIRETRIZES DE SAÍDA
- Retorne APENAS o resultado solicitado (código, testes ou análise).
- Use blocos de código Markdown claros.
- Mantenha a simplicidade (KISS/YAGNI).
- Não adicione explicações desnecessárias a menos que solicitado.
"""
        return prompt

def spawn_agent(agent_type: str, story_id: str, task_description: str, relevant_files: List[str]) -> str:
    """
    Spawna um agente especializado com contexto isolado.
    """
    project_root = find_project_root()
    if not project_root:
        return "ERRO: Projeto não encontrado."

    logger.info(f"Spawnando agente {agent_type} para a story {story_id}...")
    
    harness = AgentHarness(agent_type, story_id, project_root)
    lean_prompt = harness.prepare_context(task_description, relevant_files)
    
    # Chamada isolada à LLM com roteamento de modelo
    with console.status(f"[bold cyan]Agente {agent_type}[/bold cyan] consultando inteligência...", spinner="dots12"):
        result = call_llm(lean_prompt, agent_type=agent_type)
    
    # 2. Lógica de Recursive Handoff (Delegação)
    if "[DELEGATE:" in result:
        import re
        handoffs = re.findall(r"\[DELEGATE:\s*(\w+)\s*\|\s*([^\]]+)\]", result)
        for sub_type, sub_task in handoffs:
            logger.info(f"Handoff detectado: {agent_type} -> {sub_type}")
            sub_result = spawn_agent(sub_type, story_id, sub_task, relevant_files)
            # Inserir o resultado do sub-agente de volta no resultado original ou processar
            result = result.replace(f"[DELEGATE: {sub_type} | {sub_task}]", f"\n### RESULTADO DA DELEGAÇÃO ({sub_type}):\n{sub_result}")
            # Recursão: O resultado com o sub-resultado pode precisar de nova análise
            # Por simplicidade aqui, apenas concatenamos, mas em MAS complexos teríamos novo loop.

    # Salvar resultado no harness para auditoria
    (harness.harness_dir / "output.md").write_text(result, encoding="utf-8")
    (harness.harness_dir / "input_prompt.md").write_text(lean_prompt, encoding="utf-8")
    
    return result

def validate_and_fix(agent_type: str, story_id: str, task_description: str, relevant_files: List[str], validation_cmd: Optional[str] = None, max_retries: int = 3) -> str:
    """
    Executa um agente, valida o resultado com um comando e tenta corrigir se falhar.
    Detecta automaticamente o framework de testes se nenhum comando for fornecido.
    """
    project_root = find_project_root()
    
    # 1. Detecção inteligente de sensor via Agente (Harness Sensor Detection)
    if not validation_cmd:
        logger.info("Solicitando ao Architecture Agent para detectar o framework de testes...")
        
        # Obter lista de arquivos ignorando diretórios pesados (node_modules, etc)
        ignore_dirs = {".git", ".asdlc", "node_modules", "venv", "build", "dist", "__pycache__", "target"}
        files = []
        for p in project_root.rglob("*"):
            if p.is_file() and not any(d in p.parts for d in ignore_dirs):
                files.append(str(p.relative_to(project_root)))
                if len(files) >= 50: break
        file_list_str = "\n".join(files)

        detection_prompt = f"""
Analise o PROJECT_CONTEXT.md e a estrutura de arquivos abaixo para determinar qual comando de teste deve ser usado para validar a story {story_id}.
IMPORTANTE: Ignore o PROJECT_CONTEXT.md se ele contradisser a estrutura real de arquivos. 
Se você ver arquivos .ino, pode ser um projeto Arduino (use 'arduino-cli' se disponível ou sugira um).
Se você ver arquivos .py, use pytest.

ESTRUTURA DE ARQUIVOS REAL:
{file_list_str}

Responda APENAS com o comando de execução (ex: 'pytest', 'npm test', 'go test').
Se não houver framework configurado ou se for um tipo de projeto que você não conhece o comando de cabeça, responda 'CREATE_SUGGESTION'.
"""
        detected_cmd = spawn_agent("architecture", story_id, detection_prompt, ["PROJECT_CONTEXT.md"])
        
        if "CREATE_SUGGESTION" in detected_cmd:
            logger.warning("Nenhum framework detectado. Solicitando plano de configuração...")
            suggestion_prompt = f"O projeto não possui testes. Sugira um framework e comandos de configuração para a story {story_id}."
            return spawn_agent("architecture", story_id, suggestion_prompt, [])
        
        validation_cmd = detected_cmd.strip().strip("'").strip('"')
        from .utils import live_print
        live_print(f"[bold cyan]Framework detectado:[/bold cyan] {validation_cmd}")

    harness = AgentHarness(agent_type, story_id, project_root)
    
    current_task = task_description
    attempt = 0
    
    while attempt < max_retries:
        logger.info(f"Tentativa {attempt + 1} para o agente {agent_type}...")
        
        prompt = harness.prepare_context(current_task, relevant_files)
        result = call_llm(prompt, agent_type=agent_type)
        
        # Simular a aplicação do resultado (em um sistema real, salvaríamos os arquivos)
        # Por enquanto, apenas rodamos a validação se o comando for fornecido
        
        try:
            logger.info(f"Rodando validação: {validation_cmd}")
            # Em um cenário real, o comando rodaria sobre os arquivos modificados
            process = subprocess.run(validation_cmd, shell=True, capture_output=True, text=True, cwd=project_root)
            
            if process.returncode == 0:
                logger.info("OK: Validação passou!")
                return result
            else:
                logger.warning(f"ERRO: Validação falhou (Tentativa {attempt + 1})")
                error_feedback = f"A validação falhou com o seguinte erro:\n{process.stderr}\n{process.stdout}\nPor favor, corrija o código."
                current_task = f"{task_description}\n\n### FEEDBACK DE ERRO:\n{error_feedback}"
                attempt += 1
        except Exception as e:
            logger.error(f"Erro ao executar validação: {e}")
            break
            
    return "Falha ao atingir conformidade após retries."
