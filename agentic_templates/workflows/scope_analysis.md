---
description: Workflow para análise de escopo e quebra de stories grandes em sub-stories quando necessário.
---

# 📋 ANÁLISE DE ESCOPO (`/asdlc-plan`)

Use quando precisa implementar algo complexo e quer que o agente:
1. Analise o escopo da solicitação
2. Decida se uma única story é suficiente ou se precisa de subtarefas
3. Crie múltiplas stories relacionadas se necessário

## Quando Usar

- A solicitação é ampla (" preciso de um sistema de auth completo")
- Há múltiplas partes claramente separáveis (frontend + backend + tests)
- Quer validar o plano antes de começar a implementar

## Como Usar

```
Você: "/asdlc-plan Preciso adicionar sistema de auth com login, registro, recuperação de senha e OAuthGoogle"
```

## Passos da Workflow

### Passo 1: Análise de Escopo
1. O agente identifica os componentes necessários
2. Separa em categorias lógicas:
   - **Core**: Estrutura base, modelos, database
   - **UI**: Telas, componentes visuais
   - **API**: Endpoints, validações
   - **Integration**: OAuth, serviços externos
   - **Tests**: Testes unitários, integração, e2e

### Passo 2: Decisão de Quebra
O agente decide:

**Uma única story** se:
- Escopo pequeno/médio
- Componentes fortemente acoplados
- Pode ser implementado em 1-2 sessões

**Múltiplas stories (subtasks)** se:
- Múltiplas sessões de trabalho necessárias
- Componentes fracamente acoplados
- Uma depende da outra logicamente
- Equipe precisa trabalhar em paralelo

### Passo 3: Criação das Stories

Se decidir por múltiplas stories:

```markdown
# Story 1: Auth Core (v1)
---
title: "Auth v1 - Modelos e Database"
ticket: "20260410_AUTH_V1"
status: "PENDENTE"
depends_on: []
---

# Story 2: Auth UI (v2)
---
title: "Auth v2 - Telas de Login/Registro"
ticket: "20260411_AUTH_V2"
status: "PENDENTE"
depends_on: ["20260410_AUTH_V1"]
---

# Story 3: Auth API (v3)
---
title: "Auth v3 - Endpoints REST"
ticket: "20260412_AUTH_V3"
status: "PENDENTE"
depends_on: ["20260410_AUTH_V1"]
---

# Story 4: OAuth Google (v4)
---
title: "Auth v4 - OAuth Google"
ticket: "20260413_AUTH_V4"
status: "PENDENTE"
depends_on: ["20260412_AUTH_V3"]
---
```

### Passo 4: Apresentação ao Humano

O agente apresenta:
```
"Análise de escopo para 'Sistema de Auth':

IDENTIFICADO: 4 componentes principais
DECISÃO: Quebrar em 4 stories sequenciais

Story 1 (Core): Modelos DB + JWT setup
  → Dependencies: []
  → Estimativa: 2h

Story 2 (UI): Login + Registro + Esqueci senha
  → Dependencies: [Story 1]
  → Estimativa: 3h

Story 3 (API): Endpoints REST
  → Dependencies: [Story 1]
  → Estimativa: 2h

Story 4 (OAuth): Google OAuth
  → Dependencies: [Story 3]
  → Estimativa: 2h

TOTAL: ~9h de implementação

Aprova este plano?
[A] Criar todas as stories
[B] Ajustar escopo
[C] Cancelar
"
```

## Regras de Decisão

### Quebrar em subtarefas quando:
- Tempo estimado > 4h total
- Múltiplas tecnologias diferentes (DB + UI + API)
- Equipe pode trabalhar em paralelo
- Uma parte bloqueia outra

### Manter em uma story quando:
- Tempo estimado < 2h
- Componentes fortemente relacionados
- Mesmo arquivo/tecnologia
- Uma pessoa faz tudo

## pós-Aprovação

Após aprovado:
1. Use `/asdlc-execute` na primeira story (v1)
2. Após completar, Execute a próxima (v2)
3. Repita até todas concluídas
