# asdlc/plan_generator.py (versão Arquiteto de Software)
import logging
from pathlib import Path
from .llm_client import call_llm
from .utils import get_project_structure

logger = logging.getLogger(__name__)


def gerar_plano_de_execucao(story_data: dict, project_root: Path) -> str:
    """
    Usa uma LLM para atuar como arquiteto e gerar um plano de execução completo.
    """
    logger.info(f"Iniciando planejamento com IA para a story: {story_data.get('title')}")

    # 1. Coletar contexto do projeto (com limite de segurança)
    try:
        context_file = project_root / "PROJECT_CONTEXT.md"
        if context_file.exists():
            # Limitar contexto a 3000 caracteres para evitar estouro de tokens
            project_context = context_file.read_text(encoding="utf-8")
            if len(project_context) > 3000:
                project_context = project_context[:3000] + "\n... (contexto truncado para economizar tokens)"
        else:
            project_context = "Nenhum PROJECT_CONTEXT.md fornecido."
    except Exception as e:
        project_context = f"Erro ao ler PROJECT_CONTEXT.md: {e}"

    # 2. Obter estrutura de arquivos (já otimizada no utils.py)
    project_structure = get_project_structure(project_root)

    # 2. Determinar se é uma Bug Story para ajustar o prompt
    is_bug = story_data.get("type") == "bug_fix"

    # 3. Construir o prompt de "Arquiteto" para a LLM
    # Textos condicionais para bugs (fora do f-string para evitar syntax errors)
    bug_rule = (
        "4.  **PARA BUGS:** Você DEVE incluir uma seção de 'Análise de Causa Raiz (RCA)' e priorizar a criação de um 'Teste de Regressão' que reproduza o erro antes do fix."
        if is_bug
        else "4.  (Bugs não aplicam-se a este projeto)"
    )
    bug_example = (
        """
    **Bug Fix API:**
    - Título: "Erro 500 no endpoint de Login"
    - Descrição: "O endpoint /auth/login falha quando o email contém caracteres especiais"
    - **RCA:** Falha na regex de validação que não cobre caracteres unicode.
    - **Manifesto:** `src/auth/validator.py`, `tests/test_auth_bugs.py`
    - **Tarefas:** Criar teste de reprodução, ajustar regex, validar sanitzation
    - **Critérios:** Teste de regressão passa, endpoint retorna 400 para emails inválidos e 200 para unicode válidos
    """
        if is_bug
        else ""
    )

    prompt = f"""
    **PERSONA:** Você é um Arquiteto de Software Sênior e especialista no framework A-SDLC.

    {"**MODO DEBUG:** Estamos tratando um BUG. Seu objetivo principal é a identificação da causa raiz (RCA) e a criação de testes de regressão." if is_bug else ""}

    **TAREFA:** Sua missão é transformar uma solicitação de alto nível em um plano de execução detalhado em Markdown. Você deve analisar a solicitação, considerar o contexto do projeto e, o mais importante, **criar um Manifesto de Arquivos específico e acionável com os arquivos de CÓDIGO FONTE necessários.**

    **REGRAS CRÍTICAS:**
    1.  Seu foco é **EXCLUSIVAMENTE** na solicitação do usuário.
    2.  O Manifesto de Arquivos deve conter **APENAS arquivos de código fonte** (ex: `.html`, `.py`, `.js`, `.css`, etc.) ou de configuração (ex: `Dockerfile`, `requirements.txt`).
    3.  **NUNCA** inclua arquivos do próprio framework A-SDLC (como `.md` da pasta `.asdlc/` ou `stories/`) no Manifesto.
    {bug_rule}
    5.  **CONSIDERE O TIPO DE PROJETO:**
       - `web_frontend`: Use HTML, CSS, JavaScript (ex: `index.html`, `style.css`, `script.js`)
       - `web_api`: Use Python/Node.js (ex: `app.py`, `requirements.txt` ou `server.js`, `package.json`)
       - `web_fullstack`: Combine frontend e backend
       - `mobile`: Use React Native/Flutter (ex: `App.js`, `package.json`)
       - `desktop`: Use Electron/Python GUI (ex: `main.js`, `index.html`)
       - `cli`: Use Python/Node.js CLI (ex: `main.py`, `requirements.txt`)
    6.  **TRACER BULLETS (FATIAS VERTICAIS)**: Organize as tarefas como fatias verticais que atravessam todas as camadas. Cada tarefa deve ser funcional e testável independentemente.
       - **CORRETO**: "Tarefa 1: Modelo User + endpoint POST /users + teste de integração"
       - **EVITAR**: "Tarefa 1: Criar todos os modelos. Tarefa 2: Criar todos os endpoints. Tarefa 3: Criar todos os testes"
       - O objetivo é obter feedback imediato sobre se a integração funciona.
    7.  **MÓDULOS PROFUNDOS**: Prefira módulos com interfaces simples que escondem complexidade interna. Evite módulos "rasos" onde cada função expõe detalhes internos.
       - **PROFUNDO**: Uma função `cache.get(key)` que esconde conexão, TTL, fallback, retry
       - **RASO**: `cache.connect()`, `cache.prepare()`, `cache.execute()`, `cache.close()`
       - Módulos profundos são mais fáceis para agentes de IA navegarem e manterem.

    **EXEMPLOS DE BONS RESULTADOS POR TIPO:**
    ---
    {bug_example}

    **Web Frontend:**
    - Título: "Implementar relógio analógico HTML"
    - Descrição: "Criar uma página web estática que exibe um relógio analógico funcional e estilizado"
    - **Manifesto:** `index.html`, `style.css`, `script.js`
    - **Tarefas:** Estrutura HTML, design CSS, lógica JavaScript
    - **Critérios:** Design responsivo, animações suaves, JavaScript puro

    **Web API:**
    - Título: "Otimizar Cache InfluxDB com Sistema Unificado"
    - Descrição: "Implementar cache unificado por tipo de dados com rate limiting"
    - **Manifesto:** `app/services/influxdb_smart_cache.py`, `app/services/influxdb_service.py`
    - **Tarefas:** Cache unificado, rate limiting, métricas de performance
    - **Critérios:** Redução de 60% no tempo de resposta, cache hit rate > 80%

    **Mobile App:**
    - Título: "App de lista de tarefas React Native"
    - Descrição: "Aplicativo móvel para gerenciar tarefas com persistência local"
    - **Manifesto:** `App.js`, `package.json`, `components/TodoList.js`, `services/storage.js`
    - **Tarefas:** Interface React Native, persistência AsyncStorage, componentes reutilizáveis
    - **Critérios:** Interface intuitiva, persistência de dados, performance otimizada

    **Desktop App:**
    - Título: "Aplicativo desktop de gerenciamento de arquivos"
    - Descrição: "Criar aplicativo desktop para organizar e gerenciar arquivos"
    - **Manifesto:** `main.js`, `index.html`, `package.json`, `src/fileManager.js`
    - **Tarefas:** Interface Electron, gerenciamento de arquivos, UX desktop
    - **Critérios:** Interface intuitiva, performance otimizada, instalação simples

    **CLI App:**
    - Título: "CLI para gerenciamento de projetos"
    - Descrição: "Criar interface de linha de comando para criar, listar e remover projetos"
    - **Manifesto:** `main.py`, `requirements.txt`, `cli/commands.py`
    - **Tarefas:** Parsing de argumentos, comandos CRUD, formatação de saída
    - **Critérios:** CLI intuitiva, help detalhado, tratamento de erros

    ---
    **ENTRADAS DO ARQUITETO:**

    1. DADOS DA STORY:
       - **ID:** {story_data.get('id', 'N/A')}
       - **Título:** {story_data.get('title', 'N/A')}
       - **Descrição:** {story_data.get('description', 'N/A')}
       - **Tipo:** {story_data.get('type', 'user_story')}
       - **Critérios de Aceitação:** {story_data.get('acceptance_criteria') or 'Não especificado'}
       - **Prioridade:** {story_data.get('priority', 'Medium')}
       - **Estimativa:** {story_data.get('estimate') or 'Não especificado'}
       - **Arquivos sugeridos para criar:** {story_data.get('files_to_create') or 'Nenhum'}
       - **Arquivos sugeridos para modificar:** {story_data.get('files_to_modify') or 'Nenhum'}

    2. CONTEXTO DO PROJETO:
    {project_context}

    3. ESTRUTURA ATUAL DE ARQUIVOS DO PROJETO:
    {project_structure}
"""

    # 3. Chamar a LLM com roteamento para Arquiteto
    plano_gerado = call_llm(prompt, agent_type="architecture")

    return plano_gerado
