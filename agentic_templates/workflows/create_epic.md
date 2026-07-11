---
description: Workflow para criação de Épicos no A-SDLC. Um Épico representa um objetivo estratégico de alto nível que agrupa múltiplas stories com valor de negócio independente. Use apenas quando o pedido é realmente de dimensão de roadmap.
---

# 🏔️ CRIAR ÉPICO A-SDLC (`/asdlc-create-epic`)

Use este comando quando o pedido representa um **objetivo estratégico macro** — algo com horizonte de semanas ou múltiplos sprints, onde cada parte entregue já tem valor de negócio autônomo.

> **Épico não é sinônimo de "story grande" ou "muitas stories dependentes".**
> Stories encadeadas com `depends_on` são um grafo de entrega normal — não um épico.
> Um épico existe quando o objetivo em si é grande o suficiente para ter entrada própria no roadmap do produto.

## Quando Usar

- O pedido usa verbos de roadmap: "lançar", "construir o módulo de", "criar a plataforma de"
- Múltiplos domínios funcionais distintos, cada um com valor independente
- Horizonte percebido de semanas, com múltiplos ciclos de entrega
- O scope_gate ou o grill diagnosticou ÉPICO

## Quando NÃO Usar

- Stories com `depends_on` encadeadas (isso é grafo de entrega, use `/asdlc-plan`)
- Feature grande mas com objetivo único (use `/asdlc-plan` com tracer bullets)

---

## Passos do Workflow

### Passo 0: Injeção de Contexto Mínima (MANDATÓRIO)

Leia **apenas**:
1. `stories/MEMORY.md` — verificar se já existe um épico relacionado em andamento (seção "Épicos Ativos")
2. `GLOSSARY.md` — garantir que o objetivo usa a linguagem ubíqua do projeto

> **Token-safe**: não leia PROJECT_CONTEXT nem ADRs neste momento. São lidos opcionalmente no Passo 2.

---

### Passo 1: Definição do Objetivo Estratégico

Trabalhe com o humano (ou interprete o contexto) para definir:

```
🏔️ ÉPICO: [Nome do Épico]

OBJETIVO: [Uma frase — o valor de negócio que este épico entrega ao final]

CRITÉRIOS DE CONCLUSÃO DO ÉPICO:
- [ ] [O que "pronto" significa no nível macro]
- [ ] [Não são critérios de story individual — são objetivos do épico inteiro]

ESCOPO (domínios funcionais incluídos):
- [Domínio A]: descrição
- [Domínio B]: descrição

FORA DE ESCOPO (explícito):
- [O que este épico NÃO inclui]
```

---

### Passo 2: Decomposição em Stories

Decomponha o épico em **tracer bullets verticais** (cada story é funcional de ponta a ponta):

```
Story 1: [título] — [domínio/slice]
  Depende de: []
  Estimativa: ~Xh

Story 2: [título] — [domínio/slice]
  Depende de: [Story 1]
  Estimativa: ~Xh

Story N: ...

TOTAL ESTIMADO: ~Xh
```

> **Regra**: Máximo 8 stories por épico na decomposição inicial. Se precisar de mais, questione se o épico deveria ser dividido em dois épicos.

---

### Passo 3: Apresentação e Aprovação (OBRIGATÓRIA)

O agente apresenta o plano consolidado e **para para aprovação**:

```
🏔️ [ÉPICO] [Nome]

OBJETIVO: [objetivo estratégico]

DECOMPOSIÇÃO EM [N] STORIES:
  1. [Título] (~Xh) → depende de: []
  2. [Título] (~Xh) → depende de: [1]
  ...

TOTAL ESTIMADO: ~Xh

Aprovar este plano?
[S] Sim — criar épico + todas as stories automaticamente
[N] Não — ajustar [o quê]
[P] Parcial — criar épico agora, stories depois
```

**Aguarde a resposta antes de qualquer criação de arquivo.**

---

### Passo 4: Criação Autônoma (pós-aprovação [S] ou [P])

Após aprovação, o agente executa **sem novas interrupções**:

#### 4.1 — Criar arquivo do épico

Crie `stories/epics/EPIC_YYYYMMDD_NOME.md` com a estrutura:

```markdown
---
title: "[OBJETIVO EM POUCAS PALAVRAS]"
epic_id: "EPIC_YYYYMMDD_NOME"
status: "EM ANDAMENTO"
created: "YYYY-MM-DD"
---

# 🏔️ Épico: [Título]

## 🎯 Objetivo Estratégico
[Uma frase — o valor de negócio que este épico entrega]

## 📋 Critérios de Conclusão
- [ ] [Critério macro 1]
- [ ] [Critério macro 2]

## 🚫 Fora de Escopo
- [Item 1]

## 🗺️ Stories Filhas
| Story ID | Título | Status | Depende De |
|----------|--------|--------|------------|
| [preenchido após criar stories] | | | |

## 📝 Decisões e Notas
[Decisões arquiteturais específicas do épico — atualizado ao longo da execução]
```

#### 4.2 — Criar cada story filha

Para cada story aprovada, invoque `/asdlc-create-story` com o campo `epic_id` preenchido no frontmatter.

#### 4.3 — Atualizar tabela de stories no arquivo do épico

Após criar todas as stories, volte ao arquivo do épico e preencha a tabela "Stories Filhas" com os IDs reais gerados.

#### 4.4 — Atualizar MEMORY.md

Adicione o épico à seção "Épicos Ativos" do `stories/MEMORY.md`:

```markdown
| EPIC_YYYYMMDD_NOME | [objetivo em 5 palavras] | EM ANDAMENTO | 0/N concluídas |
```

Adicione também as stories filhas nas seções "Pendentes" normais do MEMORY.

---

### Passo 5: Relatório Final (compacto)

```
✅ Épico criado: stories/epics/EPIC_YYYYMMDD_NOME.md
✅ [N] stories criadas em stories/

Ordem de execução sugerida:
  1. [Story_A] → /asdlc-execute [ID]
  2. [Story_B] → aguarda Story_A
  ...

Próximo passo: /asdlc-execute [primeira story]
```

---

## Regras do Agente

1. **Épico é exceção, não regra**: Se houver dúvida interna, use `/asdlc-plan` em vez de épico.
2. **Aprovação única**: Pede aprovação apenas uma vez (Passo 3). Depois cria tudo autonomamente.
3. **MEMORY é suficiente para rastreio**: O progresso do épico é lido via MEMORY.md (tabela flat de ~10 tokens/épico). Só abra o arquivo de épico quando precisar de detalhes específicos.
4. **Máximo 8 stories por épico** na decomposição inicial. Mais que isso indica escopo mal-definido — considere dividir em dois épicos.
5. **Atualização do Épico ao concluir stories**: O agente de implementação DEVE atualizar a tabela "Stories Filhas" no arquivo do épico e a contagem em MEMORY.md ao marcar uma story como CONCLUÍDO.
