# Plano de Refatoração e Implementação do A-SDLC (Abordagem Híbrida)

Este documento detalha os passos para refatorar o `asdlc_framework.py` e implementar um novo workflow híbrido (CLI + Interativo).

## 📋 Visão Geral da Refatoração

### Objetivo Principal
Transformar o script monolítico `asdlc_framework.py` em uma ferramenta de linha de comando (CLI) híbrida que segue o padrão de ferramentas de desenvolvimento modernas:

1. **Modo CLI (Padrão)**: Quando executado com comandos e argumentos (ex: `python asdlc_framework.py create-story`), executa a tarefa diretamente
2. **Modo Interativo (Fallback)**: Quando executado sem comandos (`python asdlc_framework.py`), apresenta menu amigável

### Funcionalidade Central
A funcionalidade central continua sendo a **geração de um plano de execução detalhado** dentro de um arquivo Markdown de "story", agora com templates de agentes específicos.

---

## 🚀 Fase 1: Refatoração da Estrutura e Modularização

O objetivo é quebrar a classe monolítica `ASDLCFramework` em módulos com responsabilidades únicas.

### Passo 1.1: Criar Módulos de Lógica

**Estrutura de Diretórios:**
```
asdlc/
├── __init__.py
├── project_manager.py      # Lógica de initialize_project e open_existing_project
├── story_manager.py        # Lógica de create_story e list_stories
├── plan_generator.py       # Nova lógica de gerar_plano_de_execucao
├── ui_manager.py           # Lógica de show_banner e show_menu
├── code_generator.py       # Lógica de geração de código
├── test_runner.py          # Lógica de execução de testes
├── code_reviewer.py        # Lógica de code review
├── deploy_manager.py       # Lógica de deploy
└── config_manager.py       # Gerenciamento de configurações
```

**Tarefas Específicas:**
- Criar a pasta `asdlc/` no diretório raiz
- Mover métodos da classe `ASDLCFramework` para módulos apropriados
- Implementar interfaces claras entre módulos
- Manter compatibilidade com funcionalidades existentes

### Passo 1.2: Implementar o Ponto de Entrada Híbrido

**Novo arquivo `main.py`:**
```python
#!/usr/bin/env python3
"""
A-SDLC Framework - Ponto de Entrada Híbrido
"""

import argparse
import sys
from asdlc.ui_manager import UIManager
from asdlc.project_manager import ProjectManager
from asdlc.story_manager import StoryManager

def main():
    parser = argparse.ArgumentParser(description="A-SDLC Framework")
    parser.add_argument("command", nargs="?", help="Comando a executar")
    parser.add_argument("--project-name", help="Nome do projeto")
    parser.add_argument("--story-title", help="Título da story")
    # ... outros argumentos
    
    args = parser.parse_args()
    
    if args.command:
        # Modo CLI
        execute_cli_command(args)
    else:
        # Modo Interativo
        ui_manager = UIManager()
        ui_manager.show_menu()

def execute_cli_command(args):
    """Executa comando CLI"""
    if args.command == "create-project":
        project_manager = ProjectManager()
        project_manager.initialize_project(
            name=args.project_name
        )
    elif args.command == "create-story":
        story_manager = StoryManager()
        story_manager.create_story(
            title=args.story_title
        )
    # ... outros comandos

if __name__ == "__main__":
    main()
```

---

## 🎯 Fase 2: Implementação do Core - Gerador de Planos

Esta é a feature central da nova visão.

### Passo 2.1: Implementar `plan_generator.py`

**Estrutura do Módulo:**
```python
# asdlc/plan_generator.py

class PlanGenerator:
    def __init__(self):
        self.agents_dir = Path(".asdlc/agents")
        self.templates_dir = Path(".asdlc/templates")
    
    def gerar_plano_de_execucao(self, story_data: dict) -> str:
        """Gera plano de execução detalhado em Markdown"""
        
        # Template do Markdown com frontmatter
        template = f"""---
status: "📝 Criada"
story_id: "{story_data['id']}"
created_at: "{story_data['created_at']}"
---

# 📝 Story: {story_data['title']}

## 📋 Informações Básicas
- **ID**: {story_data['id']}
- **Tipo**: {story_data['type']}
- **Título**: {story_data['title']}
- **Prioridade**: {story_data['priority']}
- **Estimativa**: {story_data['estimate']} horas
- **Status**: 📝 Criada
- **Data**: {story_data['created_at']}

## 📝 Descrição
{story_data['description']}

## ✅ Critérios de Aceitação
{story_data['acceptance_criteria']}

## 🔄 Plano de Execução Detalhado

### 1. 📊 Análise de Requisitos
- [ ] **Agente de Análise** - Analisar requisitos da story
- [ ] **Agente de Análise** - Definir escopo e dependências
- [ ] **Agente de Análise** - Identificar riscos técnicos

### 2. 🏗️ Design da Arquitetura
- [ ] **Agente de Arquitetura** - Definir componentes necessários
- [ ] **Agente de Arquitetura** - Planejar integrações
- [ ] **Agente de Arquitetura** - Documentar decisões técnicas

### 3. 💻 Desenvolvimento
- [ ] **Agente de Código** - Gerar código com IA
- [ ] **Agente de Código** - Implementar funcionalidade
- [ ] **Agente de Código** - Seguir padrões do projeto

### 4. 🧪 Testes
- [ ] **Agente de Testes** - Testes unitários
- [ ] **Agente de Testes** - Testes de integração
- [ ] **Agente de Testes** - Testes de aceitação

### 5. 🔍 Code Review
- [ ] **Agente de Review** - Revisão de código
- [ ] **Agente de Review** - Validação de qualidade
- [ ] **Agente de Review** - Aprovação

### 6. 🚀 Deploy
- [ ] **Agente de Deploy** - Preparar para produção
- [ ] **Agente de Deploy** - Deploy automatizado
- [ ] **Agente de Deploy** - Monitoramento

## 📊 Métricas
- **Tempo de Desenvolvimento**: 
- **Cobertura de Testes**: 
- **Qualidade do Código**: 
- **Performance**: 

## 📝 Notas
- 

## 🔗 Links Relacionados
- 

---
*Story criada com A-SDLC Framework*
"""
        return template
```

### Passo 2.2: Criar os Templates de Agente

**Estrutura de Templates:**
```
.asdlc/
├── agents/
│   ├── analysis_agent.md
│   ├── architecture_agent.md
│   ├── code_agent.md
│   ├── test_agent.md
│   ├── review_agent.md
│   └── deploy_agent.md
└── templates/
    ├── story_template.md
    ├── project_template.md
    └── config_template.yml
```

**Exemplo de Template de Agente (`analysis_agent.md`):**
```markdown
# Agente de Análise de Requisitos

## Responsabilidades
- Analisar requisitos da story
- Definir escopo e dependências
- Identificar riscos técnicos
- Validar viabilidade

## Entrada
- Descrição da story
- Critérios de aceitação
- Contexto do projeto

## Saída
- Análise detalhada de requisitos
- Lista de dependências
- Identificação de riscos
- Estimativas de complexidade

## Critérios de Sucesso
- [ ] Requisitos claramente definidos
- [ ] Dependências identificadas
- [ ] Riscos documentados
- [ ] Estimativas validadas
```

---

## 🔧 Fase 3: Reconstrução da Interface (CLI e Interativa)

### Passo 3.1: Construir os Comandos CLI

**Comandos Principais:**
```bash
# Gerenciamento de Projetos
python asdlc_framework.py create-project --name "meu-projeto"
python asdlc_framework.py open-project --name "projeto-existente"
python asdlc_framework.py list-projects

# Gerenciamento de Stories
python asdlc_framework.py create-story --title "Nova funcionalidade"
python asdlc_framework.py list-stories
python asdlc_framework.py implement-story --id "story-id"

# Agentes de IA
python asdlc_framework.py setup-agents
python asdlc_framework.py generate-code --type "api" --description "..."

# Desenvolvimento
python asdlc_framework.py run-tests
python asdlc_framework.py review-code
python asdlc_framework.py deploy

# Utilitários
python asdlc_framework.py show-metrics
python asdlc_framework.py show-docs
```

**Implementação no `main.py`:**
```python
def setup_cli_parser():
    parser = argparse.ArgumentParser(description="A-SDLC Framework")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comandos de projeto
    project_parser = subparsers.add_parser("create-project", help="Criar novo projeto")
    project_parser.add_argument("--name", required=True, help="Nome do projeto")
    project_parser.add_argument("--description", help="Descrição do projeto")
    project_parser.add_argument("--type", default="web_api", help="Tipo do projeto")
    
    # Comandos de story
    story_parser = subparsers.add_parser("create-story", help="Criar nova story")
    story_parser.add_argument("--title", required=True, help="Título da story")
    story_parser.add_argument("--description", help="Descrição da story")
    story_parser.add_argument("--type", default="user_story", help="Tipo da story")
    
    # ... outros comandos
    
    return parser
```

### Passo 3.2: Reconstruir o Menu Interativo

**Implementação no `ui_manager.py`:**
```python
class UIManager:
    def __init__(self):
        self.project_manager = ProjectManager()
        self.story_manager = StoryManager()
    
    def show_menu(self):
        """Mostra menu interativo"""
        self.show_banner()
        
        while True:
            self.display_menu_options()
            choice = input("🎯 Escolha uma opção: ")
            
            try:
                self.execute_menu_choice(choice)
                if choice == "0":
                    break
            except KeyboardInterrupt:
                print("\n👋 Saindo...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    def execute_menu_choice(self, choice):
        """Executa escolha do menu - chama as mesmas funções dos comandos CLI"""
        if choice == "1":
            # Chama a mesma função que o comando CLI create-project
            self.project_manager.initialize_project()
        elif choice == "3":
            # Chama a mesma função que o comando CLI create-story
            self.story_manager.create_story()
        # ... outras opções
```

---

## 🧹 Fase 4: Limpeza e Documentação Final

### Passo 4.1: Remover Código Legado

**Tarefas:**
- Eliminar completamente a classe `ASDLCFramework` original
- Remover funções redundantes após modularização
- Limpar imports não utilizados
- Atualizar referências nos testes

**Arquivos a serem removidos/modificados:**
- `asdlc_framework.py` (será substituído por `main.py`)
- Remover métodos duplicados nos novos módulos
- Limpar configurações obsoletas

### Passo 4.2: Atualizar o `README.md`

**Nova Documentação:**
```markdown
# 🚀 A-SDLC Framework

## Uso Híbrido (CLI + Interativo)

### Modo CLI (Recomendado para automação)
```bash
# Criar projeto
python asdlc_framework.py create-project --name "meu-projeto"

# Criar story
python asdlc_framework.py create-story --title "Nova funcionalidade"

# Listar stories
python asdlc_framework.py list-stories

# Executar testes
python asdlc_framework.py run-tests
```

### Modo Interativo (Para descoberta)
```bash
python asdlc_framework.py
# Apresenta menu amigável com todas as opções
```

## Estrutura do Projeto
```
asdlc/
├── __init__.py
├── project_manager.py
├── story_manager.py
├── plan_generator.py
├── ui_manager.py
└── ...

.asdlc/
├── agents/
│   ├── analysis_agent.md
│   ├── code_agent.md
│   └── ...
└── templates/
    ├── story_template.md
    └── ...
```
```

---

## 📅 Cronograma de Implementação

### Semana 1: Fase 1
- [ ] Criar estrutura de módulos
- [ ] Implementar `project_manager.py`
- [ ] Implementar `story_manager.py`
- [ ] Implementar `ui_manager.py`

### Semana 2: Fase 2
- [ ] Implementar `plan_generator.py`
- [ ] Criar templates de agentes
- [ ] Testar geração de planos

### Semana 3: Fase 3
- [ ] Implementar comandos CLI
- [ ] Reconstruir menu interativo
- [ ] Testar ambos os modos

### Semana 4: Fase 4
- [ ] Limpar código legado
- [ ] Atualizar documentação
- [ ] Testes finais
- [ ] Release

---

## 🎯 Critérios de Sucesso

### Funcional
- [ ] Comandos CLI funcionam corretamente
- [ ] Menu interativo mantém funcionalidade
- [ ] Geração de planos funciona
- [ ] Templates de agentes implementados

### Técnico
- [ ] Código modular e limpo
- [ ] Sem duplicação de lógica
- [ ] Documentação atualizada
- [ ] Testes passando

### UX
- [ ] Interface intuitiva
- [ ] Mensagens de erro claras
- [ ] Feedback adequado
- [ ] Compatibilidade com uso existente

---

## 🔧 Comandos de Desenvolvimento

### Para Desenvolvedores
```bash
# Executar em modo desenvolvimento
python -m asdlc.main

# Executar testes
python -m pytest tests/

# Verificar qualidade de código
python -m black asdlc/
python -m flake8 asdlc/
```

### Para Usuários
```bash
# Instalar
pip install -e .

# Usar CLI
asdlc create-project --name "meu-projeto"

# Usar modo interativo
asdlc
```

---

*Este plano garante uma transição suave do framework atual para a nova arquitetura híbrida, mantendo todas as funcionalidades existentes enquanto adiciona as novas capacidades de CLI e geração de planos detalhados.* 