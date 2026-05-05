---
title: "VisualFeedbackUI"
ticket: "20260426_004628_visualfeedbackui"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: VisualFeedbackUI

**História do Usuário:** Implementar funcionalidade: VisualFeedbackUI

## 📝 Especificações da Story

Como usuário do framework A-SDLC, quero receber feedback visual claro e intuitivo durante a execução dos comandos CLI (criação de projetos, geração de planos, execução de agentes, validação), para entender rapidamente o progresso, o status e possíveis erros, melhorando a experiência de uso e a confiança no sistema.

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:**
  - `asdlc/feedback_ui.py`
  - `asdlc/feedback_themes.py`
  - `tests/test_feedback_ui.py`
- **MODIFICAR:**
  - `asdlc/ui_manager.py`
  - `asdlc/plan_generator.py`
  - `asdlc/agent_executor.py`
  - `asdlc/project_manager.py`
  - `main.py`

## 🎯 Tarefas Detalhadas

### Tarefa 1: Criar Componente Base de Feedback Visual
1. **Arquivo a criar**: `asdlc/feedback_ui.py`
2. **Referência de Contexto**: `pyproject.toml` (já possui `rich` como dependência)
3. **Ação**: Implementar a classe `FeedbackUI` usando `rich` para exibir barras de progresso, spinners, tabelas e painéis estilizados.

#### 1.1 Definição da Classe Base
```python
# asdlc/feedback_ui.py
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import Optional, List, Dict
import sys
import time

console = Console()

class FeedbackUI:
    """Fornece feedback visual rico para operações CLI do A-SDLC."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.progress = None
        self._current_task = None

    def start_spinner(self, message: str):
        """Inicia um spinner com mensagem."""
        console.print(f"[bold blue]⏳ {message}[/bold blue]")
    
    def stop_spinner(self, message: str, success: bool = True):
        """Para o spinner e exibe resultado."""
        icon = "✅" if success else "❌"
        console.print(f"  {icon} {message}")

    def progress_bar(self, total: int, description: str):
        """Retorna um gerenciador de contexto para barra de progresso."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=True,
        )

    def print_table(self, title: str, columns: List[str], rows: List[List[str]]):
        """Exibe uma tabela formatada."""
        table = Table(title=title, box=box.ROUNDED)
        for col in columns:
            table.add_column(col, style="cyan")
        for row in rows:
            table.add_row(*row)
        console.print(table)

    def print_panel(self, message: str, style: str = "bold green"):
        """Exibe uma mensagem em destaque."""
        console.print(Panel(message, style=style))

    def print_error(self, message: str):
        """Exibe uma mensagem de erro."""
        console.print(f"[bold red]❌ {message}[/bold red]")
    
    def print_warning(self, message: str):
        """Exibe um aviso."""
        console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")

    def print_success(self, message: str):
        """Exibe uma mensagem de sucesso."""
        console.print(f"[bold green]✅ {message}[/bold green]")
```

### Tarefa 2: Implementar Temas de Feedback
1. **Arquivo a criar**: `asdlc/feedback_themes.py`
2. **Ação**: Definir estilos e temas pré-configurados para diferentes tipos de operação (criação de projeto, geração de plano, execução, validação).

#### 2.1 Definição de Temas
```python
# asdlc/feedback_themes.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class FeedbackTheme:
    name: str
    spinner_message: str
    success_message: str
    error_prefix: str
    color: str
    icon: str

THEMES = {
    "project_creation": FeedbackTheme(
        name="Criação de Projeto",
        spinner_message="Criando estrutura do projeto...",
        success_message="Projeto criado com sucesso!",
        error_prefix="Falha na criação",
        color="green",
        icon="📁"
    ),
    "plan_generation": FeedbackTheme(
        name="Geração de Plano",
        spinner_message="Gerando plano de execução...",
        success_message="Plano gerado com sucesso!",
        error_prefix="Falha na geração do plano",
        color="blue",
        icon="🧠"
    ),
    "agent_execution": FeedbackTheme(
        name="Execução de Agente",
        spinner_message="Executando agente...",
        success_message="Agente concluído!",
        error_prefix="Falha na execução do agente",
        color="magenta",
        icon="🤖"
    ),
    "validation": FeedbackTheme(
        name="Validação",
        spinner_message="Executando validações...",
        success_message="Validação concluída!",
        error_prefix="Falha na validação",
        color="yellow",
        icon="🛡️"
    )
}
```

### Tarefa 3: Integrar Feedback Visual no Fluxo Principal
1. **Arquivos a modificar**: `asdlc/ui_manager.py`, `asdlc/plan_generator.py`, `asdlc/agent_executor.py`, `asdlc/project_manager.py`, `main.py`
2. **Ação**: Substituir prints simples por chamadas ao `FeedbackUI` em todas as etapas de interação com o usuário.

#### 3.1 Modificar `main.py`
```python
# main.py (trecho modificado)
from asdlc.feedback_ui import FeedbackUI

feedback = FeedbackUI(verbose=True)

def main():
    feedback.print_panel("🚀 A-SDLC Framework - AI-Driven Software Development Lifecycle", style="bold cyan")
    # ... lógica de menu com feedback visual
```

#### 3.2 Modificar `asdlc/plan_generator.py`
```python
# asdlc/plan_generator.py (trecho)
from asdlc.feedback_ui import FeedbackUI
from asdlc.feedback_themes import THEMES

feedback = FeedbackUI()

class PlanGenerator:
    def generate_plan(self, story):
        theme = THEMES["plan_generation"]
        feedback.start_spinner(f"{theme.icon} {theme.spinner_message}")
        try:
            # lógica de geração
            feedback.stop_spinner(theme.success_message, success=True)
        except Exception as e:
            feedback.stop_spinner(f"{theme.error_prefix}: {str(e)}", success=False)
            raise
```

### Tarefa 4: Adicionar Testes Unitários para Feedback Visual
1. **Arquivo a criar**: `tests/test_feedback_ui.py`
2. **Ação**: Testar todas as funções de feedback visual, garantindo que as saídas sejam formatadas corretamente e que os temas sejam aplicáveis.

#### 4.1 Exemplo de Teste
```python
# tests/test_feedback_ui.py
import pytest
from asdlc.feedback_ui import FeedbackUI
from asdlc.feedback_themes import THEMES

def test_feedback_ui_initialization():
    fb = FeedbackUI(verbose=True)
    assert fb.verbose is True

def test_feedback_theme_integrity():
    for key, theme in THEMES.items():
        assert theme.name is not None
        assert theme.color is not None
```

## ✅ Critérios de Aceitação

- [ ] A CLI exibe barras de progresso animadas durante operações longas (criação de projeto, geração de plano, execução de agentes).
- [ ] Todas as mensagens de erro, sucesso e aviso usam formatação rica (cores, ícones) em vez de texto simples.
- [ ] Os temas de feedback são consistentes e facilmente customizáveis.
- [ ] A performance da CLI não é impactada negativamente (overhead < 5%).
- [ ] Os testes unitários cobrem 100% das novas funcionalidades de feedback visual.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `FeedbackUI` para a classe principal
  - `FeedbackTheme` para os temas
  - `rich` como biblioteca de renderização
- ❌ **NUNCA USAR**:
  - `print()` diretamente para feedback do usuário
  - Cores fixas sem suporte a temas

### **Estrutura de Código**:
- Usar type hints em todas as funções públicas
- Seguir o estilo de código PEP 8
- Manter a compatibilidade com Python 3.8+

## 🎨 Princípios a Seguir

- **Segurança**: Nenhuma informação sensível deve ser exposta nas barras de progresso.
- **Performance**: Spinners e barras de progresso devem ser leves e não bloquear a execução.
- **Logging**: Todas as operações de feedback devem ser registradas no logger para depuração.
- **Modularidade**: O sistema de feedback deve ser independente e facilmente desacoplável.
- **Reutilização**: Os temas devem ser reutilizáveis em qualquer módulo do framework.

## 📊 Métricas de Sucesso

### **Performance**:
- Inicialização do `FeedbackUI` em < 50ms
- Renderização de tabela com 1000 linhas em < 100ms

### **Estabilidade**:
- Zero crashes relacionados ao feedback visual em 100 execuções consecutivas
- Tratamento adequado de redirecionamento de saída (pipes, arquivos)

### **Experiência do Usuário**:
- Redução de 30% no tempo de compreensão do status das operações
- Feedback positivo em pesquisa de usabilidade (média > 4/5)

## ⏱️ Plano de Implementação

### **Fase 1: Implementação do Módulo Feedback (2 horas)**
1. Criar `feedback_ui.py` com a classe base
2. Criar `feedback_themes.py` com os temas padrão
3. Testar manualmente com script de demonstração

### **Fase 2: Integração com Módulos Existentes (3 horas)**
1. Modificar `main.py` para usar `FeedbackUI`
2. Integrar no `plan_generator.py`
3. Integrar no `agent_executor.py`
4. Integrar no `project_manager.py`

### **Fase 3: Testes e Documentação (1 hora)**
1. Escrever testes unitários
2. Atualizar `README.md` com exemplos de feedback visual
3. Verificar métricas de performance

**Tempo Total Estimado**: 6 horas
**Impacto**: Alto para experiência do usuário
**Risco**: Baixo (biblioteca `rich` já incluída como dependência)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Analise se há problemas potenciais com a renderização do `rich` em diferentes terminais (Windows, Linux, macOS) e verifique se a lógica de fallback para terminais não suportados está adequada."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos listados no Manifesto. Use `rich` para toda renderização visual. Siga todos os padrões e princípios definidos."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes que capturem a saída do console e validem a presença de elementos específicos (ícones, cores, barras de progresso). Teste os temas e a integridade das mensagens."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Revise o código para garantir que não há `print()` residual, que todos os caminhos de exceção estão cobertos com feedback visual adequado e que a performance não foi degradada."

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."