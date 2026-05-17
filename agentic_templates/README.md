# 🤖 A-SDLC Agentic Mode Guide (v2.4.0)

## O que é este diretório?

O A-SDLC Agentic Mode é uma forma de usar o framework diretamente dentro da sua IDE (Cursor, Windsurf, Cline, RooCode) **sem precisar de Python**. A metodologia é injetada diretamente no agente de IA.

Em vez de rodar um CLI para gerar markdowns e depois alimentar uma IA, **você copia os templates para o seu projeto e usa comandos no chat da IDE**.

---

## 📥 Como Instalar

> [!IMPORTANT]
> **A maioria dos comandos (`/asdlc-grill`, `/asdlc-create-story`, `/asdlc-execute`, etc.) não requer Python.** São puramente baseados em templates de texto que o agente interpreta.
>
> **Exceção: `/asdlc-dashboard`** — este comando gera um HTML interativo e requer o `main.py` (framework Python completo).

### Instalação sem Python (recomendada para a maioria)

Copie apenas a pasta de templates para o seu projeto:
```bash
cp -r agentic_templates/ seu-projeto/
```
*(Opcional) Renomeie para `.agents/` se sua IDE suportar.*

### Instalação com Python (necessária apenas para `/asdlc-dashboard`)

Clone o repositório completo:
```bash
git clone https://github.com/jota-f/asdlc-framework.git
cd asdlc-framework
pip install -r requirements.txt
```
Ou copie os templates e também os arquivos do núcleo:
```
seu-projeto/
├── agentic_templates/   ← templates (sem Python)
├── asdlc/               ← núcleo Python (apenas para dashboard)
└── main.py              ← ponto de entrada CLI
```

---

## 🚀 Quick Start

### Comandos disponíveis

| Comando | Quando Usar |
|---------|-------------|
| `/asdlc-grill` | Questionamento guiado para demandas vagas |
| `/asdlc-architecture` | Perguntas de arquitetura e modelagem |
| `/asdlc-plan` | Analisar escopo grande e quebrar em stories |
| `/asdlc-create-story` | Criar uma story formal |
| `/asdlc-execute` | Implementar uma story (TDD obrigatório) |
| `/asdlc-bug` | Diagnosticar e corrigir bugs |
| `/asdlc-dashboard` | Gerar dashboard visual do projeto (KPIs, Kanban, Burndown) |

---

## 📋 Workflow Completo

### Fase 1: Validação de Requisitos (se demanda vaga)
> **Você:** `/asdlc-grill Quero adicionar cache no sistema`

O agente questiona: quem usa? qual endpoint? qual métrica? etc.

### Fase 2: Descoberta Arquitetural (opcional)
> **Você:** `/asdlc-architecture WebSocket ou Server-Sent Events para notificações?`

O agente discute opções e recomenda a melhor abordagem.

### Fase 3: Planejamento (para features grandes)
> **Você:** `/asdlc-plan Preciso de auth completo: login, registro, recuperação, OAuth`

O agente quebra em múltiplas stories sequenciais.

### Fase 4: Criação da Story
> **Você:** `/asdlc-create-story Sistema de notificações via WebSocket`

O agente cria a story em `stories/` seguindo o template A-SDLC.

### Fase 5: Implementação (TDD)
> **Você:** `/asdlc-execute`

O agente executa o ciclo completo:
1. Verifica dependências
2. Cria testes que FALHAM (Red Phase)
3. Implementa código até testes passarem (Green Phase)
4. Valida critérios de aceitação
5. Marca story como CONCLUÍDO

### Fase 6: Dashboard Visual (opcional)
> **Você:** `/asdlc-dashboard`

> [!WARNING]
> Este comando requer o framework Python completo (`main.py` + pasta `asdlc/`).
> Se só tiver os templates copiados, o agente irá gerar um **resumo em texto** das métricas no próprio chat em vez do HTML interativo.

**Com Python instalado** — o agente executa `python main.py dashboard --no-open` e gera:
- Arquivo `.asdlc/dashboard/dashboard.html` com KPIs, Kanban, Burndown e Velocity
- Abre automaticamente no browser

**Sem Python (só templates)** — o agente lê as stories e reporta no chat:
- KPIs: total de stories, concluídas, pendentes
- Stories bloqueadas por dependências
- Stories sem critérios de aceitação

> [!TIP]
> O HTML gerado é auto-contido. Abra em qualquer browser sem instalar nada. Pode ser compartilhado por e-mail ou Slack.

---

## 🔗 Sistema de Dependências

Stories podem ter dependências via campo `depends_on`:

```yaml
---
title: "Dashboard com Gráficos"
ticket: "20260408_DASH"
status: "PENDENTE"
depends_on: ["20260407_NOTIFY"]
---
```

**Regras:**
- Story só executa se todas dependências = `CONCLUÍDO`
- Agente verifica automaticamente antes de implementar

---

## 🆕 Novidades (v2.4.0)

| Feature | Descrição |
|---------|-----------|
| `/asdlc-dashboard` | Dashboard visual interativo do projeto (KPIs, Kanban, Burndown) |
| `asdlc_dashboard` | Skill para gerar e interpretar o dashboard no modo agentic |
| `templates/` | Pasta dedicada para templates e exemplos (separado das stories ativas) |
| `/asdlc-grill` | Questionamento proativo para demandas vagas |
| TDD Obrigatório | Pipeline: Red → Green → Refactor |
| Tracer Bullets | Fatias verticais (DB → API → UI) |
| Smart Zone | Monitoramento de contexto (80k/100k tokens) |
| Deep Modules | Orientação de arquitetura (interfaces simples) |
| `/asdlc-bug` | Workflow de resolução de bugs com RCA |
| `asdlc_bug_hunter` | Skill de diagnóstico e causa raiz |

---

## 📁 Estrutura de Arquivos

```
agentic_templates/
├── README.md                    # Este arquivo (PT)
├── README_EN.md                 # Versão em inglês
├── TOOL_GUIDE.md               # Guia de otimização de tokens
├── validate_stories.py         # Validador de estrutura de stories
├── skills/
│   ├── asdlc_story_generator/  # Requirements Agent - criar stories
│   ├── asdlc_implementation/   # Code Agent - implementar (TDD)
│   ├── asdlc_context_compactor/# Compactar contexto longo
│   ├── asdlc_bug_hunter/       # Bug Hunter - diagnóstico e RCA
│   └── asdlc_dashboard/        # Dashboard visual do projeto
├── workflows/
│   ├── grill_requirements.md   # Questionamento guiado
│   ├── architecture_discovery.md # Descoberta arquitetural
│   ├── scope_analysis.md       # Análise de escopo
│   ├── create_asdlc_story.md   # Criação de story
│   ├── implement_asdlc_story.md # Implementação TDD
│   ├── bug_resolution.md       # Resolução de bugs
│   └── dashboard.md            # Dashboard visual do projeto
├── templates/
│   ├── story_template.md       # Template padrão de story
│   ├── bug_template.md         # Template padrão de bug
│   └── exemplo/                # Exemplos de stories
└── stories/
    └── MEMORY.md               # Memória do projeto
```

---

## ⚡ Otimização de Tokens

### Dicas
1. **MEMORY.md primeiro** - visão geral sem iterar todas stories
2. **PROJECT_CONTEXT** - inclua apenas seção relevante
3. **Context Compactor** - invoque após 30+ mensagens
4. **Smart Zone** - mantenha contexto < 80k tokens

### Smart Zone vs Dumb Zone
| Zona | Tokens | Comportamento |
|------|--------|---------------|
| Smart | < 80k | IA precisa |
| Warning | 80k-100k | Qualidade degrada |
| Dumb | > 100k | IA comete erros |

---

## ⚙️ Requisitos

- IDE com suporte a agentes AI (Cursor, Windsurf, Cline, RooCode)
- Pasta `.agents/` ou equivalente (opcional)
- **Não requer Python ou dependências**

---

## 📖 Mais Informações

- **[TOOL_GUIDE.md](TOOL_GUIDE.md)** - Otimização de tools e tokens
- **[stories/MEMORY.md](stories/MEMORY.md)** - Memória do projeto
- **[templates/exemplo/README.md](templates/exemplo/README.md)** - Guia de versionamento
