# 🌌 A-SDLC Framework (v2.4.0)
**AI-Driven Software Development Lifecycle**

O A-SDLC é um framework que transforma assistentes de IA em agentes autônomos capazes de gerenciar o ciclo de vida completo de um projeto de software. Ele utiliza **Harness Engineering**, **TDD Obrigatório**, **Tracer Bullets** e **Feedback Loops** para garantir código de alta fidelidade.

---

## Sumário

- [O que é o A-SDLC?](#o-que-é-o-a-sdlc)
- [Três Formas de Usar](#três-formas-de-usar)
- [Instalação](#instalação)
- [Modo Antigravity (Gratuito)](#modo-antigravity-gratuito)
- [Modo API Externa (Autônomo)](#modo-api-externa-autônomo)
- [Modo Agentic (Sem Python)](#modo-agentic-sem-python)
- [Workflow Completo](#workflow-completo)
- [Comandos CLI](#comandos-cli)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Estrutura de um Projeto](#estrutura-de-um-projeto)
- [Conceitos Chave](#conceitos-chave)
- [Exemplos](#exemplos)
- [Termos de Uso](#termos-de-uso)

---

## O que é o A-SDLC?

Diferente de assistentes de chat, o A-SDLC trata a IA como um **Sistema Multi-Agente (MAS)**. Cada tarefa é executada por agentes especialistas (Requisitos, Arquitetura, Código, Testes, Review) que validam o trabalho uns dos outros.

### Pilares do Framework

| Pilar | Descrição |
|-------|-----------|
| **Harness Engineering** | Cada agente opera em ambiente isolado com contexto enxuto e sensores de validação |
| **TDD Obrigatório** | Testes são criados ANTES do código (Red → Green → Refactor) |
| **Tracer Bullets** | Tarefas atravessam todas as camadas (DB → API → UI) para feedback imediato |
| **Smart Zone** | Monitoramento de contexto para manter a LLM na zona de precisão (<80k tokens) |
| **Recursive Handoffs** | Agentes delegam subtarefas entre si via `[DELEGATE: tipo | tarefa]` |

---

## Três Formas de Usar

| | 🧠 Antigravity (IDE) | ⚡ API Externa (CLI) | 📋 Agentic (Templates) |
|---|---|---|---|
| **Quem pensa?** | A IDE (Cursor/Windsurf) | API OpenAI/OpenRouter | A IDE (chat) |
| **Custo** | Gratuito | Pago (tokens) | Gratuito |
| **Complexidade** | Média (MCP server) | Baixa (CLI) | Mínima (copy/paste) |
| **Autonomia** | Semi-autônomo | 100% autônomo | Semi-autônomo |
| **Ideal para** | Projetos grandes | Automação total | Protó rápido |

---

## Instalação

### Requisitos
- Python 3.10+
- Git

### Passo 1: Clonar e instalar dependências
```bash
git clone https://github.com/jota-f/A-SDLC.git
cd A-SDLC
pip install -r requirements.txt
```

### Passo 2: Configurar variáveis de ambiente
```bash
cp .env.example .env
```
Edite o `.env` conforme o modo que deseja usar (veja abaixo).

### Passo 3 (Opcional): Configurar MCP para IDE
```bash
pip install fastmcp mcp
```
Adicione ao `mcp_config.json` da sua IDE:
```json
"asdlc": {
  "command": "python",
  "args": ["C:/Caminho/Para/A-SDLC/asdlc/mcp_server.py"],
  "env": { "PYTHONPATH": "C:/Caminho/Para/A-SDLC" }
}
```

---

## Modo Antigravity (Gratuito)

Neste modo, a IDE é o "cérebro". O MCP serve como ferramenta de gestão.

### Configuração
```env
ASDLC_ENGINE=antigravity
```

### Ferramentas MCP disponíveis
| Ferramenta | Função |
|---|---|
| `asdlc_create_project` | Inicializa um projeto |
| `asdlc_create_story` | Cria uma story |
| `asdlc_get_story_details` | Lê conteúdo de uma story |
| `asdlc_update_story_status` | Atualiza status |
| `asdlc_list_stories` | Lista stories |
| `asdlc_get_project_metrics` | Métricas de progresso |
| `asdlc_validate_project` | Valida conformidade |

### Como implementar
No chat da IDE:
> *"Use a Skill @asdlc_implementation para implementar a story @stories/ID"*

---

## Modo API Externa (Autônomo)

O script Python assume o controle total, usando a API OpenAI/OpenRouter para spawnar agentes.

### Configuração
```env
ASDLC_ENGINE=external
OPENROUTER_API_KEY=sua_chave_aqui
# ou
OPENAI_API_KEY=sua_chave_aqui
```

### Ferramentas MCP adicionais
| Ferramenta | Função |
|---|---|
| `asdlc_implement_story` | Execução autônoma via agentes |
| `asdlc_spawn_specialist` | Invoca agente ad-hoc |

### Como implementar
```bash
python main.py implement --id 20260425_204837
```

---

## Modo Agentic (Sem Python)

Copia a metodologia A-SDLC diretamente para o seu projeto. Sem dependências Python.

### Instalação
```bash
cp -r agentic_templates/ seu-projeto/
```

### Comandos disponíveis no chat da IDE
| Comando | Quando Usar |
|---------|-------------|
| `/asdlc-grill` | Questionamento guiado para demandas vagas |
| `/asdlc-architecture` | Perguntas de arquitetura |
| `/asdlc-plan` | Quebrar features grandes em stories |
| `/asdlc-create-story` | Criar story formal |
| `/asdlc-execute` | Implementar uma story |
| `/asdlc-bug` | Diagnosticar e corrigir bugs |

### Fluxo típico
```
1. /asdlc-grill              → Validar requisitos (se demanda vaga)
2. /asdlc-architecture       → Definir abordagem
3. /asdlc-plan               → Quebrar em stories
4. /asdlc-create-story       → Criar story
5. /asdlc-execute            → Implementar (TDD automático)
```

---

## Workflow Completo

### Cenário A: Projeto Novo
```bash
python main.py create-project --name "meu_app" --prompt "Descrição do app"
```

### Cenário B: Projeto Existente
```bash
python main.py create-project --name "meu_projeto" --path "C:/pasta/do/projeto" --prompt "Análise"
```

### Cenário C: Criar Story
```bash
python main.py create-story --title "Implementar Login"
```

### Cenário D: Implementar Story (TDD)
```bash
python main.py implement --id 20260504_120000_implementar_login
```

### Cenário E: Listar Stories
```bash
python main.py list-stories
```

### Cenário F: Validar Projeto
```bash
python main.py validate --format markdown
```

---

## Comandos CLI

| Comando | Descrição | Argumentos |
|---------|-----------|------------|
| `create-project` | Inicializa novo projeto | `--name`, `--prompt`, `--type`, `--path` |
| `create-story` | Cria uma story | `--title` |
| `implement` | Executa implementação TDD | `--id` |
| `list-stories` | Lista todas as stories | — |
| `validate` | Valida conformidade | `--project`, `--format`, `--output` |

### Modo interativo (sem argumentos)
```bash
python main.py
```
Exibe um menu interativo com todas as opções.

---

## Variáveis de Ambiente

### Obrigatórias
| Variável | Descrição |
|----------|-----------|
| `ASDLC_ENGINE` | `antigravity` (padrão) ou `external` |
| `OPENROUTER_API_KEY` | Chave OpenRouter (quando `external`) |
| `OPENAI_API_KEY` | Chave OpenAI (quando `external`, fallback) |

### Opcionais (modo external)
| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `OPENAI_MODEL` | `gpt-4.1-mini` | Modelo padrão |
| `OPENAI_MAX_TOKENS` | `4096` | Limite de tokens |
| `OPENAI_TEMPERATURE` | `0.3` | Temperatura |
| `MODEL_CODE` | — | Modelo para Code Agent |
| `MODEL_ARCH` | — | Modelo para Architecture Agent |
| `MODEL_TEST` | — | Modelo para Test Agent |
| `MODEL_REQ` | — | Modelo para Requirements Agent |
| `MODEL_REVIEW` | — | Modelo para Review Agent |

---

## Estrutura de um Projeto

```
meu-projeto/
├── .asdlc/
│   ├── agents/              # 6 personas de agentes
│   │   ├── code_agent.md
│   │   ├── test_agent.md
│   │   ├── architecture_agent.md
│   │   ├── requirements_agent.md
│   │   ├── review_agent.md
│   │   └── bug_hunter_agent.md
│   └── harness/             # Output dos agentes (execução)
├── stories/                 # Stories + MEMORY.md
│   └── MEMORY.md
├── prompts/                 # Templates de prompts LLM
├── PROJECT_CONTEXT.md       # Blueprint do projeto
├── BACKLOG.md               # Débitos técnicos (auto-gerado)
└── src/                     # Código do projeto
```

---

## Conceitos Chave

### Pipeline TDD (Obrigatório)
```
Architecture → Test Red → Code Green → Validation → Review
```
- **Red**: Testes são criados e FALHAM (especificação executável)
- **Green**: Código é implementado até os testes passarem
- **Refactor**: Melhoria de código com testes protegendo

### Smart Zone vs Dumb Zone
| Zona | Tokens | Comportamento |
|------|--------|---------------|
| Smart Zone | < 80k | IA precisa |
| Warning | 80k-100k | Qualidade degrada |
| Dumb Zone | > 100k | IA comete erros bobos |

### Tracer Bullets (Fatias Verticais)
```
CORRETO: Modelo + Endpoint + Teste (uma story)
EVITAR: Todos os modelos → Todos os endpoints → Todos os testes
```

### Lei Inviolável
**NUNCA** marque uma story como DONE sem um `run_command` retornando exit code 0.

---

## Exemplos

### 🚗 Sensor de Fadiga (Arduino/ESP32)
- **Local**: `test_projects/drowsinessSensor`
- Sensores de feedback para validar compilação de firmware

### 📝 TodoList Fullstack
- **Local**: `examples/web_fullstack`
- Fluxo completo de requisitos até teste E2E

---

## Termos de Uso

Licença MIT com restrição: **Uso comercial proibido sem autorização**.
- **Livre**: Uso pessoal, acadêmico e open-source
- **Atribuição**: Obrigatório citar "Desenvolvido com A-SDLC Framework"

---

**A-SDLC: Onde o código não é apenas escrito, ele é projetado por máquinas e validado por regras.**
