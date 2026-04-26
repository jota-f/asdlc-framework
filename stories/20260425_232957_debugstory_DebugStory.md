---
title: "DebugStory"
ticket: "20260425_232957_debugstory"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: DebugStory

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: DebugStory

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:** `src/debug/debug_story.py`, `src/debug/__init__.py`
- **MODIFICAR:** `src/cli.py` (para integrar o novo comando)

## 🎯 Tarefas Detalhadas

### Tarefa 1: Criar módulo de depuração de stories
1. **Arquivo a criar/modificar**: `src/debug/__init__.py`, `src/debug/debug_story.py`
2. **Referência de Contexto**: O framework A-SDLC gerencia stories em arquivos `.md` na pasta `stories/`. A funcionalidade de depuração deve permitir listar, inspecionar e re-executar stories com logs detalhados.
3. **Ação**: Criar o pacote `src/debug/` e implementar a classe `DebugStory` com métodos para listar stories, exibir detalhes e re-executar com rastreamento.

#### 1.1 Criar `src/debug/__init__.py`
```python
# src/debug/__init__.py
from .debug_story import DebugStory

__all__ = ["DebugStory"]
```

#### 1.2 Criar `src/debug/debug_story.py`
```python
# src/debug/debug_story.py
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class DebugStory:
    """
    Classe para depuração de stories no framework A-SDLC.
    Permite listar, inspecionar e re-executar stories com logs detalhados.
    """
    
    def __init__(self, stories_dir: str = "stories"):
        self.stories_dir = stories_dir
        self.debug_log: List[Dict] = []
    
    def list_stories(self) -> List[str]:
        """Lista todos os arquivos de story disponíveis."""
        if not os.path.exists(self.stories_dir):
            return []
        return [f for f in os.listdir(self.stories_dir) if f.endswith(".md")]
    
    def inspect_story(self, story_name: str) -> Optional[Dict]:
        """Inspeciona os detalhes de uma story específica."""
        story_path = os.path.join(self.stories_dir, story_name)
        if not os.path.exists(story_path):
            return None
        
        with open(story_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "name": story_name,
            "path": story_path,
            "content": content,
            "size": len(content)
        }
    
    def re_run_story(self, story_name: str) -> Dict:
        """Re-executa uma story com rastreamento detalhado."""
        start_time = datetime.now()
        
        # Simula a re-execução (aqui seria integrado com o Agent Executor)
        result = {
            "story": story_name,
            "started_at": start_time.isoformat(),
            "status": "executing",
            "steps": []
        }
        
        # Exemplo de passo de depuração
        step = {
            "step": "parse_story",
            "status": "success",
            "duration_ms": 150,
            "details": "Story parsed successfully"
        }
        result["steps"].append(step)
        
        # Finaliza
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() * 1000
        result["status"] = "completed"
        result["duration_ms"] = duration
        result["completed_at"] = end_time.isoformat()
        
        # Registra no log de depuração
        self.debug_log.append(result)
        
        return result
    
    def get_debug_log(self) -> List[Dict]:
        """Retorna o log completo de depuração."""
        return self.debug_log
    
    def clear_debug_log(self) -> None:
        """Limpa o log de depuração."""
        self.debug_log = []
```

### Tarefa 2: Integrar comando de depuração no CLI
1. **Arquivo a criar/modificar**: `src/cli.py`
2. **Ação**: Adicionar um subcomando `debug` ao CLI existente para acessar as funcionalidades de depuração.

#### 2.1 Modificar `src/cli.py` para incluir o comando debug
```python
# src/cli.py (modificação - adicionar no final do arquivo)
import argparse
from src.debug import DebugStory

def add_debug_parser(subparsers):
    """Adiciona o subcomando debug ao parser principal."""
    debug_parser = subparsers.add_parser("debug", help="Ferramentas de depuração para stories")
    debug_subparsers = debug_parser.add_subparsers(dest="debug_command", required=True)
    
    # Subcomando: list
    list_parser = debug_subparsers.add_parser("list", help="Lista todas as stories disponíveis")
    
    # Subcomando: inspect
    inspect_parser = debug_subparsers.add_parser("inspect", help="Inspeciona uma story específica")
    inspect_parser.add_argument("story_name", type=str, help="Nome do arquivo da story")
    
    # Subcomando: re-run
    rerun_parser = debug_subparsers.add_parser("re-run", help="Re-executa uma story com rastreamento")
    rerun_parser.add_argument("story_name", type=str, help="Nome do arquivo da story")
    
    # Subcomando: log
    log_parser = debug_subparsers.add_parser("log", help="Exibe o log de depuração")
    log_parser.add_argument("--clear", action="store_true", help="Limpa o log de depuração")

def handle_debug_command(args):
    """Manipula os comandos de depuração."""
    debugger = DebugStory()
    
    if args.debug_command == "list":
        stories = debugger.list_stories()
        if stories:
            print("Stories disponíveis:")
            for story in stories:
                print(f"  - {story}")
        else:
            print("Nenhuma story encontrada.")
    
    elif args.debug_command == "inspect":
        details = debugger.inspect_story(args.story_name)
        if details:
            print(f"Story: {details['name']}")
            print(f"Tamanho: {details['size']} caracteres")
            print("--- Conteúdo ---")
            print(details['content'][:500] + "..." if len(details['content']) > 500 else details['content'])
        else:
            print(f"Story '{args.story_name}' não encontrada.")
    
    elif args.debug_command == "re-run":
        result = debugger.re_run_story(args.story_name)
        print(f"Re-execução de '{args.story_name}':")
        print(f"  Status: {result['status']}")
        print(f"  Duração: {result.get('duration_ms', 0):.2f}ms")
        print("  Passos:")
        for step in result.get("steps", []):
            print(f"    - {step['step']}: {step['status']} ({step.get('duration_ms', 0)}ms)")
    
    elif args.debug_command == "log":
        if args.clear:
            debugger.clear_debug_log()
            print("Log de depuração limpo.")
        else:
            log = debugger.get_debug_log()
            if log:
                print("Log de depuração:")
                for entry in log:
                    print(f"  - Story: {entry['story']}, Status: {entry['status']}, Duração: {entry.get('duration_ms', 0):.2f}ms")
            else:
                print("Log de depuração vazio.")
```

## ✅ Critérios de Aceitação

- [ ] O módulo `DebugStory` é importável e funcional sem erros
- [ ] O comando `debug list` lista corretamente as stories disponíveis
- [ ] O comando `debug inspect <story>` exibe detalhes da story especificada
- [ ] O comando `debug re-run <story>` executa e retorna rastreamento detalhado
- [ ] O comando `debug log` exibe o histórico de depuração
- [ ] O comando `debug log --clear` limpa o histórico de depuração
- [ ] Todos os comandos tratam erros (ex: story não encontrada) adequadamente

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `DebugStory` para a classe principal
  - `debug` para o subcomando CLI
  - `stories` para o diretório de stories
  - `re-run` para re-execução

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - Nomes genéricos como `utils` ou `helpers`
  - Caminhos absolutos para diretórios
  - Variáveis globais mutáveis

### **Estrutura de Código**:
- Seguir padrão de classes com type hints
- Documentar métodos com docstrings
- Usar `os.path.join` para caminhos
- Tratar exceções com try/except específicos

## 🎨 Princípios a Seguir

- **Segurança**: Validar caminhos de arquivo para evitar path traversal
- **Performance**: Usar lazy loading para arquivos grandes
- **Logging**: Manter log detalhado de todas as operações de depuração
- **Modularidade**: Cada funcionalidade de depuração em método separado
- **Reutilização**: A classe `DebugStory` deve ser independente do CLI

## 📊 Métricas de Sucesso

### **Performance**:
- Listagem de stories em < 100ms
- Inspeção de story em < 50ms
- Re-execução com rastreamento em < 500ms

### **Estabilidade**:
- 100% dos comandos CLI funcionam sem crash
- Tratamento adequado de todos os erros de arquivo

### **Experiência do Usuário**:
- Mensagens de erro claras e informativas
- Saída formatada e legível no terminal

## ⏱️ Plano de Implementação

### **Fase 1: Módulo Core** (30 min)
1. Criar `src/debug/__init__.py`
2. Criar `src/debug/debug_story.py` com classe `DebugStory`
3. Implementar métodos: `list_stories`, `inspect_story`, `re_run_story`

### **Fase 2: Integração CLI** (20 min)
1. Modificar `src/cli.py` para adicionar subcomando `debug`
2. Implementar handlers para cada subcomando
3. Testar todos os comandos manualmente

**Tempo Total Estimado**: 50 minutos
**Impacto**: Baixo para o sistema existente (adiciona funcionalidade sem quebrar existente)
**Risco**: Baixo (funcionalidade isolada em módulo separado)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide se a RCA descrita faz sentido técnico e se o teste de reprodução cobre o cenário relatado."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários, de integração e de performance conforme as métricas de sucesso definidas."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

### **Requirements Agent (Opcional)**:
Combine a persona do `.asdlc/agents/requirements_agent.md` com a tarefa: "Analise se os requisitos foram completamente atendidos e se há gaps na implementação. Sugira melhorias se necessário."

### **Architecture Agent (Opcional)**:
Combine a persona do `.asdlc/agents/architecture_agent.md` com a tarefa: "Valide a arquitetura implementada e verifique se está alinhada com os princípios de design definidos. Sugira otimizações arquiteturais se necessário."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."