# 📋 Changelog - A-SDLC Framework

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-03-07

### Adicionado
- **🌟 Suporte Nativo a Agentes Autônomos (Agentic Mode):** Criação do diretório `agentic_templates/` fornecendo integração para ferramentas e IDEs autônomas (Cursor, Windsurf, Cline, RooCode).
- **A-SDLC Skills:** Adição das habilidades de IA `asdlc_story_generator` e `asdlc_implementation` que transicionam a cognição da IA ativamente (Arquiteto -> QA -> Coder) sem ferramentas Python externas.
- **A-SDLC Workflows:** Adição de gatilhos rápidos via chat (`/asdlc-create-story` e `/asdlc-execute`).
- **Casos de Uso Práticos:** Inserção de estudo de caso prático para uso da nova abordagem de Arquitetura -> Requisitos -> Execução.

### Modificado
- Reestruturação massiva da documentação (`README.md` e `README_EN.md`), movendo a parte visual do Modo Agentic para o topo como Método 1, rebaixando a instalação e foco do app Python-CLI.

---

## [1.0.1] - Atualizações Recentes

### Adicionado
- Sistema de validação automática de conformidade A-SDLC
- Diretório de exemplos com projetos demonstrativos
- Documentação completa do framework
- Exemplo de TodoList sem A-SDLC para comparação

### Alterado
- Melhorias na interface CLI
- Otimização do gerador de planos
- Refatoração do sistema de agentes

### Corrigido
- Bugs na criação de estrutura de projetos
- Problemas de validação de entrada
- Erros de formatação em templates

## [1.0.0] - 2024-08-03

### Adicionado
- 🚀 **Framework A-SDLC completo**
  - Sistema de 5 agentes especializados
  - Gerador de planos inteligente
  - Interface CLI moderna
  - Sistema de stories estruturado

- 🤖 **Agentes Especializados**
  - Code Agent (Desenvolvedor Sênior Full-Stack)
  - Test Agent (QA Engineer Sênior)
  - Architecture Agent (Arquiteto de Software Sênior)
  - Requirements Agent (Analista de Requisitos Sênior)
  - Review Agent (Code Reviewer Sênior)

- 📝 **Sistema de Planos**
  - Geração automática de planos detalhados
  - Templates otimizados para LLMs externas
  - Checklists de melhores práticas
  - Manifestos de arquivos específicos

- 🎯 **Tipos de Projeto Suportados**
  - web_frontend (HTML/CSS/JS, React, Vue)
  - web_api (Python FastAPI, Node.js Express)
  - web_fullstack (Frontend + Backend)
  - mobile (React Native, Flutter)
  - desktop (Electron, Tkinter)
  - cli (Aplicações linha de comando)

- 📚 **Documentação Completa**
  - README detalhado
  - PROJECT_CONTEXT.md
  - Templates de prompts
  - Guias de uso

- 🧪 **Sistema de Validação**
  - Verificação automática de implementação
  - Conformidade com padrões A-SDLC
  - Validação de testes funcionais

- 📁 **Estrutura Padronizada**
  - Diretórios organizados
  - Templates de projeto
  - Configurações A-SDLC

### Funcionalidades Principais

#### 🔄 Arquitetura Híbrida
- **Modo CLI** para automação
- **Modo Interativo** para descoberta
- **Validação em tempo real**

#### 🧠 Plan Generator
- **Stories** que se transformam em planos
- **Checklists** de melhores práticas
- **Manifestos** de arquivos específicos

#### 🤖 Agentes Especializados
- **5 personas** bem definidas
- **Responsabilidades** claras
- **Templates** otimizados

#### 📚 Prompts Profissionais
- **Templates** para ChatGPT, Gemini
- **Contexto** específico por tipo de projeto
- **Instruções** detalhadas

#### ⚡ CLI Inteligente
- **Interface moderna**
- **Validação robusta**
- **Feedback em tempo real**

#### 🎯 Conformidade Automática
- **Verificação** de padrões
- **Validação** de implementação
- **Garantia** de qualidade

### Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **OpenAI API** - Integração com GPT
- **argparse** - Interface CLI
- **PyYAML** - Configurações
- **python-dotenv** - Variáveis de ambiente

### Estrutura de Arquivos

```
A-SDLC-Framework/
├── asdlc/                    # 🧠 Core framework
│   ├── project_manager.py    # Gestão de projetos
│   ├── story_manager.py      # Gestão de stories
│   ├── plan_generator.py     # Geração de planos
│   ├── ui_manager.py         # Interface de usuário
│   └── llm_client.py         # Cliente para APIs de LLM
├── .asdlc/                   # 🤖 Configuração A-SDLC
│   └── agents/               # Agentes especializados
├── prompts/                  # 📚 Templates para LLMs
├── examples/                 # 📖 Projetos de exemplo
├── tests/                    # 🧪 Testes do framework
├── main.py                   # 🚀 Ponto de entrada
├── PROJECT_CONTEXT.md        # 📋 Contexto do framework
└── README.md                 # 📖 Documentação
```

---

## 📝 Notas de Versão

### v1.0.0 - Lançamento Inicial
- Framework completo e funcional
- Documentação abrangente
- Exemplos práticos
- Sistema de validação

### Próximas Versões Planejadas

#### v1.1.0 - Melhorias de UX
- Interface gráfica opcional
- Templates visuais
- Integração com IDEs

#### v1.2.0 - Expansão de Tipos
- Mais tipos de projeto
- Templates específicos
- Integração com mais LLMs

#### v2.0.0 - Framework Avançado
- Sistema de plugins
- API REST
- Dashboard web

---

**💡 Cada versão segue os princípios A-SDLC para garantir qualidade e consistência!** 