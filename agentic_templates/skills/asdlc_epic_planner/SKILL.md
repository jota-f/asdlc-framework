---
name: asdlc_epic_planner
description: Skill para planejamento de épicos, análise de escopo abrangente e decomposição em histórias técnicas gerenciáveis com dependências mapeadas.
user_command: /to-epic
invocation_mode: user_and_model
tags: [epic, planning, scoping, tracer-bullets, roadmap]
---

# 🏔️ A-SDLC Epic Planner Skill (`/to-epic`)

Use esta skill para analisar escopos complexos (módulos completos, grandes refatorações ou novas plataformas) e decompô-los em histórias técnicas gerenciáveis (`stories/EPIC_YYYYMMDD_NAME/`).

## 🎯 Quando Usar
- A demanda envolve múltiplos domínios funcionais ou semanas de trabalho.
- A funcionalidade precisa ser entregue em etapas incrementais e independentes (Tracer Bullets).
- Uma story única excederia 2.000 tokens de contexto ou conteria mais de 8 arquivos para modificar.

---

## 🧭 Procedimento de Decomposição

### Passo 1: Análise de Dimensão & Fronteiras
Analise o escopo e identifique:
1. **Objetivo Central do Épico**: O valor final de negócio entregue.
2. **Camadas Técnicas Afetadas**: Banco de Dados, APIs/Serviços, Interface, Infraestrutura.
3. **Fatiamento Vertical (Tracer Bullets)**:
   - Divida o épico em histórias verticais de ponta a ponta (e não apenas camadas horizontais soltas).
   - Cada história intermediária deve ser testável e entregar uma parte funcional.

### Passo 2: Estruturação do Épico
Crie o arquivo de definição do épico em `stories/EPICS/EPIC_YYYYMMDD_[NOME].md`:

```markdown
---
epic_id: EPIC_YYYYMMDD_[NOME]
title: "[TÍTULO DO ÉPICO]"
status: "PLANEJADO" # PLANEJADO | EM_ANDAMENTO | CONCLUIDO
priority: "P1|P2|P3"
stories_count: [N]
---

# 🏔️ Épico: [TÍTULO]

## 🎯 Objetivo & Impacto
[Descrição clara do objetivo e benefício para o sistema]

## 🗺️ Decomposição em Stories (Tracer Bullets)

1. **[Story 1 - Título]** (`YYYYMMDD_01_feature`)
   - **Objetivo:** [Escopo enxuto]
   - **Critério de Aceite:** [Critério testável]
   - **Dependências:** Nenhuma

2. **[Story 2 - Título]** (`YYYYMMDD_02_feature`)
   - **Objetivo:** [Escopo enxuto]
   - **Critério de Aceite:** [Critério testável]
   - **Dependências:** [Story 1]

## 🔒 Riscos & Arquitetura
- [Pontos de atenção ou ADRs necessários]
```

### Passo 3: Geração Sequencial das Stories
Após aprovação do plano do épico pelo usuário, gere cada story individual utilizando a skill `asdlc_story_generator` (`/to-story`), vinculando o campo `epic_id: EPIC_YYYYMMDD_[NOME]` no frontmatter de cada story.
