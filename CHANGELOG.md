# 📋 Changelog - A-SDLC Framework

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/), e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2.4.0] - 2026-05-17

### Adicionado
- **📊 Visual Project Dashboard (Fases 1, 2, 3 e 4)**:
  - **Zero Dependências de Produção**: Gerador de dashboard HTML estático, autocontido e ultra-veloz, ideal para visibilidade em tempo real.
  - **Gráficos Dinâmicos (Chart.js via CDN)**: Gráfico de Burndown de stories e gráfico Donut de distribuição de status das stories.
  - **Kanban Interativo de 3 Colunas**: Colunas Concluído, Pendente e Em Progresso alimentadas diretamente pelo parser de stories markdown.
  - **Métricas e KPIs Animados**: Contadores animados para Total de Stories, Progresso Geral, Tasks Concluídas e Conformidade A-SDLC.
  - **Velocity Histórica (Fase 2)**: Gráfico de barras comparando stories concluídas por semana nas últimas 8 semanas.
  - **Painel de Alertas Inteligente (Fase 3)**: Notificação e identificação em tempo real de stories bloqueadas por dependências não resolvidas (`depends_on`) e de stories sem critérios de aceitação.
  - **Workflow Agentic (/asdlc-dashboard) (Fase 4)**: Nova Skill `asdlc_dashboard` com execução em modo duplo (gera o HTML se Python estiver disponível ou reporta um resumo inteligente em texto no próprio chat da IDE).
  - **Integração CLI**: Novo subcomando CLI `python main.py dashboard` com flags `--output` e `--no-open`.
- **Otimização e Organização Estrutural (Modo Agentic)**:
  - Criado o diretório `templates/` sob `agentic_templates/` para separar os templates e exemplos das stories ativas e do `MEMORY.md`.
  - Criado o template de story padrão `story_template.md` extraído da especificação técnica da Skill `asdlc_story_generator`.
  - Movido `bug_template.md` para a pasta de templates (`templates/bug_template.md`).
  - Movida a pasta de exemplos `exemplo/` para a nova pasta de templates (`templates/exemplo/`).

### Modificado
- **🔥 Evolução do `/asdlc-grill` (Grill with Docs)**: Workflow atualizado para atuar como Arquiteto de Domínio (DDD). O agente agora realiza injeção de contexto obrigatória lendo `PROJECT_CONTEXT.md` e `GLOSSARY.md`. Adicionado verificações profundas de arquitetura (Colisão de Termos, Cardinalidade, Semântica de Estados, Regras de Deleção). O agente agora atualiza ativamente o `GLOSSARY.md` com novos termos e gera automaticamente Arquitetural Decision Records (ADRs) em `docs/adr/` antes de invocar a criação da story.
- **Validador de Stories (`validate_stories.py`)**:
  - Modificado para buscar stories recursivamente usando `rglob("*.md")`, permitindo a organização em subpastas.
  - Adicionada exclusão explícita para o arquivo `MEMORY.md`, pastas com nome `templates` e arquivos que terminem com `template.md` na busca de arquivos markdown de stories.
- **Workflows e Documentação**:
  - Atualizadas as referências ao `bug_template.md` no workflow `bug_resolution.md` para apontar para `templates/bug_template.md`.
  - Atualizados os diagramas e links nos arquivos `agentic_templates/README.md`, `agentic_templates/README_EN.md` e no blueprint principal `PROJECT_CONTEXT.md`.
  - Atualizadas as seções \"Como Instalar\" dos READMEs com as distinções da instalação sem Python (templates puros) e com Python (CLI + Dashboard), incluindo indicação do arquivo `requirements.txt`.

## [2.3.0] - 2026-05-05

### Adicionado
- **Harness Auto-Cleanup**: Limpeza automática de sessões antigas no diretório `.asdlc/harness/` (mantém as últimas 30).
- **Harness Engineering Logic**: Refatoração da lógica de gerenciamento de ambiente operacional dos agentes para maior robustez.
- **Dual-Mode Engine**: Toggle `ASDLC_ENGINE` no `.env` para alternar entre Antigravity (sem custo) e External API (OpenAI/OpenRouter).
- **Lei Inviolável**: NUNCA marcar story DONE sem `run_command` com exit code 0.
- **Categorização MCP**: Ferramentas separadas em Gestão e Execução.
- **🔥 `/asdlc-grill`**: Workflow de questionamento proativo para demandas vagas. O agente "grelha" o humano sobre requisitos antes de criar stories.
- **🧪 TDD Obrigatório**: Pipeline alterado para Architecture → Test Red → Code Green → Validation → Review. Testes são criados ANTES do código.
- **🎯 Tracer Bullets**: Orientação de fatias verticais (DB → API → UI) no plan_generator e story_generator.
- **📊 Smart Zone Monitoramento**: Funções `estimate_token_count()` e `log_context_density()` no agent_executor. Warnings em 80k tokens, errors em 100k.
- **🏗️ Deep Modules**: Orientação de arquitetura no architecture_agent e plan_generator — preferir módulos com interfaces simples que escondem complexidade.
- **🐛 Bug Hunter Agent**: Agente especialista em diagnóstico e causa raiz (RCA) com 5 Whys.
- **📋 `asdlc_bug_hunter` Skill**: Skill de resolução de bugs com workflow de 5 fases.
- **Workflow `/asdlc-bug`**: Ciclo completo de diagnóstico → reprodução → RCA → fix → regressão.

### Corrigido
- **Windows Stability**: Melhoria no tratamento de encoding (UTF-8) para evitar erros de leitura/escrita em sistemas Windows.
- **Git Hygiene**: Adição de `.kilo/` e `.asdlc/harness/` ao `.gitignore` e remoção do rastreamento de arquivos temporários.
- **Style Fixes**: Formatação completa dos módulos `agent_executor.py` e `utils.py` com `black`.
- Circuito Morto MCP-API removido da Skill.
- Falso Positivo de DONE eliminado.
- `llm_client.py` respeita `ASDLC_ENGINE`.
- **`project_manager.py`**: Bug onde `project_root` não era definida quando `project_path` era fornecido (causava `UnboundLocalError`).
- **`test_framework.py`**: Reescrito completamente — imports corrigidos para API funcional (era referências a classes que não existem).
- **`test_bug_asdlc.py`**: Adicionado mock de `call_llm` que faltava, causando hang no teste.

### Modificado
- Skill `asdlc_implementation` reescrita com ciclo TDD de 6 passos (antes 4 passos sem TDD).
- `story_manager.py` pipeline alterado de 4 para 5 etapas com TDD.
- `agent_executor.py` com monitoramento de contexto (Smart Zone).
- `story_manager.py` com `_verificar_testes_existentes()` para pular Red Phase em bug fixes.
- README.md e README_EN.md completamente reescritos com documentação das 3 formas de uso.
- agentic_templates/README.md e README_EN.md atualizados com novos comandos e features.
- `.env.example` atualizado com variáveis OpenRouter e per-agent models.
- `.gitignore` limpo e organizado.

### Removido
- Referências a `@asdlc-plan.md` e `@asdlc-coder.md` (arquivos inexistentes).
- Entradas duplicadas no `.gitignore`.

---

## [2.2.0] - 2026-04-25


### Adicionado
- **🚀 A-SDLC MCP Server**: Implementação do Model Context Protocol para integração nativa com IDEs (Cursor, Windsurf).
- **🤖 Multi-Agent Execution Engine**: Nova engine em `agent_executor.py` com suporte a **Recursive Handoffs** (`[DELEGATE]`).
- **🛡️ Harness Sensors**: Sistema de feedback em tempo real que executa testes/compilação e corrige erros automaticamente.
- **📁 Suporte a Múltiplos Projetos**: Comando `create-project` e ferramentas MCP agora aceitam `--path` customizado.
- **🧬 Agente Especialista (Spawn)**: Capacidade de invocar agentes específicos para tarefas ad-hoc via CLI e MCP.

### Modificado
- **README Revitalizado**: Novo sumário clicável, guia de integração MCP e estrutura de workspace recomendada.
- **CLI Melhorada**: Comando `implement` adicionado à interface de linha de comando.
- **Resiliência Windows**: Remoção de emojis problemáticos que causavam `UnicodeEncodeError` no terminal Windows.

### Corrigido
- Importação ausente de `Optional` no `project_manager.py`.
- Lógica de detecção de sensores agora analisa a lista real de arquivos do projeto.

---

## [2.0.0] - 2026-04-07

### Adicionado
- **🌟 `/asdlc-architecture`**: Workflow de descoberta arquitetural para perguntas livres de modelagem e design
- **🌟 `/asdlc-plan`**: Análise de escopo com quebra automática de features grandes em múltiplas stories
- **🌟 Sistema de Dependências**: Campo `depends_on` no frontmatter YAML com verificação automática
- **🌟 INDEX.md**: Índice consolidado do projeto (~200 tokens vs 5000+ de todas stories)
- **🌟 Context Compactor Skill**: Skill para reduzir tokens em sessões longas (40-50% de redução)
- **🌟 TOOL_GUIDE.md**: Guia de otimização de tools com padrão Tool Search Tool (60-85% redução)
- **🌟 Stories de Exemplo**: Exemplos completos de stories independentes e com dependências
- **🌟 Validador de Stories**: Script Python para validar estrutura de stories

### Modificado
- **Skills atualizadas**: `asdlc_story_generator` e `asdlc_implementation` agora mantêm INDEX.md atualizado
- **README atualizado**: Guia completo com Quick Start e referência de comandos
- **Template de Story**: Novo campo `depends_on` e verificação automática

### Otimização de Tokens
- Elementos cacheáveis separados dos dinâmicos
- Context budget recomendado (Sistema ~15%, Story ~25%, Histórico ~50%)
- Few-shot examples reduzidos a 2-3
- PROJECT_CONTEXT não deve ser incluído completo

---

## [0.2.0] - 2026-03-07

### Adicionado
- **🌟 Suporte Nativo a Agentes Autônomos (Agentic Mode):** Criação do diretório `agentic_templates/` fornecendo integração para ferramentas e IDEs autônomas (Cursor, Windsurf, Cline, RooCode).
- **A-SDLC Skills:** Adição das habilidades de IA `asdlc_story_generator` e `asdlc_implementation` que transicionam a cognição da IA ativamente (Arquiteto -> QA -> Coder) sem ferramentas Python externas.
- **A-SDLC Workflows:** Adição de gatilhos rápidos via chat (`/asdlc-create-story` e `/asdlc-execute`).
- **Casos de Uso Práticos:** Inserção de estudo de caso prático para uso da nova abordagem de Arquitetura -> Requisitos -> Execução.

### Modificado
- Reestruturação massiva da documentação (`README.md` e `README_EN.md`), movendo a parte visual do Modo Agentic para o topo como Método 1, rebaixando a instalação e foco do app Python-CLI.

---

## [0.1.1] - Atualizações Recentes

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

---

## [0.1.0] - 2024-08-03

### Adicionado
- 🚀 **Framework A-SDLC inicial**
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

### v0.1.0 - Lançamento Inicial
- Framework base funcional
- Documentação inicial
- Exemplos práticos
- Sistema de validação

### Próximas Versões Planejadas

#### v0.x (Fase de Desenvolvimento Ativa)
- Interface gráfica opcional
- Integração profunda com IDEs nativas
- Mais tipos de projeto e LLMs suportados

#### v1.0.0 - Lançamento Oficial (Stable)
- Sistema refinado com API REST e Dashboard web
- Casos de uso validados por comunidade em massa

---

**💡 Cada versão segue os princípios A-SDLC para garantir qualidade e consistência!** 