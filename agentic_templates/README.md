# 🤖 A-SDLC Agentic Mode Guide (v2.3.0)

## O que é este diretório?

O A-SDLC Agentic Mode é uma forma de usar o framework diretamente dentro da sua IDE (Cursor, Windsurf, Cline, RooCode) **sem precisar de Python**. A metodologia é injetada diretamente no agente de IA.

Em vez de rodar um CLI para gerar markdowns e depois alimentar uma IA, **você copia os templates para o seu projeto e usa comandos no chat da IDE**.

---

## 📥 Como Instalar

1. Acesse o seu projeto
2. Copie a pasta `agentic_templates/` para a raiz do projeto
3. (Opcional) Renomeie para `.agents/` se sua IDE suportar

```bash
cp -r agentic_templates/ seu-projeto/
```

**Resultado:**
```
seu-projeto/
├── skills/                  # Skills do A-SDLC
├── workflows/               # Workflows de comandos
├── stories/                 # Suas stories
├── TOOL_GUIDE.md            # Guia de otimização
├── validate_stories.py      # Validador de stories
└── src/                     # Seu código
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

## 🆕 Novidades (v2.3.0)

| Feature | Descrição |
|---------|-----------|
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
│   └── asdlc_bug_hunter/       # Bug Hunter - diagnóstico e RCA
├── workflows/
│   ├── grill_requirements.md   # Questionamento guiado
│   ├── architecture_discovery.md # Descoberta arquitetural
│   ├── scope_analysis.md       # Análise de escopo
│   ├── create_asdlc_story.md   # Criação de story
│   ├── implement_asdlc_story.md # Implementação TDD
│   └── bug_resolution.md       # Resolução de bugs
└── stories/
    ├── MEMORY.md               # Memória do projeto
    └── exemplo/                # Exemplos de stories
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
- **[stories/exemplo/README.md](stories/exemplo/README.md)** - Guia de versionamento
