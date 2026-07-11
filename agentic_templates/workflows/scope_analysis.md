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

0. **INJEÇÃO DE CONTEXTO & CHECKPOINT (MANDATÓRIO)**:
   Antes de responder, verifique se o arquivo `.asdlc/context_checkpoint.md` existe na raiz do projeto.
   - **Se existir**: Leia o arquivo, aplique seu contexto na memória ativa e **exclua** ou **renomeie** o arquivo (ex: para `.asdlc/context_checkpoint.consumed`) usando as ferramentas do sistema de arquivos para evitar injeções repetidas.
   - **Se não existir**: Prossiga normalmente.

   Em seguida, tente ler o `GLOSSARY.md`, o índice de decisões de arquitetura **`docs/adr/LEARNING.md`** (se não existir este índice, consulte `docs/adr/`) e o **`BACKLOG.md`**.
   - Se o `GLOSSARY.md` **não existir** ou estiver vazio, o agente DEVE alertar o usuário: *"⚠️ Nenhum glossário detectado. É altamente recomendado rodar o `/asdlc-grill` antes para garantir que a quebra de tarefas use a terminologia correta e unificada."*
   - Garanta que a quebra não viole decisões de arquitetura anteriores (aprendizados indexados).
   - **MANDATÓRIO**: O agente DEVE analisar as pendências e ideias em `BACKLOG.md` para ver se alguma refatoração ou funcionalidade futura ali anotada deve ser incluída no planejamento do escopo atual.

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

Se decidir por múltiplas stories, prefira **fatias verticais (Tracer Bullets)** — cada story atravessa DB → API → UI e é funcional independentemente:

```markdown
---
title: "Auth v1 - Login (Tracer Bullet)"
ticket: "20260410_AUTH_V1"
status: "PENDENTE"
depends_on: []
---

---
title: "Auth v2 - Registro de Usuário"
ticket: "20260411_AUTH_V2"
status: "PENDENTE"
depends_on: ["20260410_AUTH_V1"]
---

---
title: "Auth v3 - Recuperação de Senha"
ticket: "20260412_AUTH_V3"
status: "PENDENTE"
depends_on: ["20260410_AUTH_V1"]
---

---
title: "Auth v4 - OAuth Google"
ticket: "20260413_AUTH_V4"
status: "PENDENTE"
depends_on: ["20260412_AUTH_V3"]
---
```

> ⚠️ **Evite stories horizontais** (ex: Story 1 = todos os modelos, Story 2 = todos os endpoints). Cada story deve ser funcional de ponta a ponta.


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

### Tracer Bullets (Fatias Verticais)
Ao quebrar em múltiplas stories, prefira **fatias verticais** a **camadas horizontais**:
- **CORRETO**: Cada story atravessa DB → API → UI e é funcional independentemente
- **EVITAR**: Story 1 = todos os modelos, Story 2 = todos os endpoints, Story 3 = toda a UI

Exemplo de Tracer Bullet:
```
Story 1: Login (modelo User + endpoint POST /login + tela de login + teste)
Story 2: Registro (modelo User extendido + endpoint POST /register + tela de registro + teste)
Story 3: Recuperação (endpoint POST /recover + email service + tela de recuperação + teste)
```

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

## pós-Aprovação — Criação Autônoma (Passo 5)

Após o humano responder `[A]` (criar todas), o agente executa **sem novas interrupções**:

### Passo 5.1 — Validação do Grafo de Dependências

Antes de criar qualquer arquivo, valide que o grafo `depends_on` é **acíclico**:

```
Verificar: A depende de B? B depende de A? → CICLO detectado → corrigir automaticamente
Regra: depende_on só pode referenciar tickets que aparecem ANTES na ordem de criação
```

Se um ciclo for detectado, o agente:
1. Identifica e quebra o ciclo removendo a dependência mais fraca
2. Notifica o humano com 1 linha: `⚠️ Ciclo detectado em [A→B→A]. Removida dependência [B→A].`
3. Prossegue sem interrupção

### Passo 5.2 — Criação Sequencial das Stories

Para cada story na ordem topológica (dependências primeiro):

1. Invocar `/asdlc-create-story` com a especificação da story
2. Confirmar que o arquivo foi salvo em `stories/`
3. Prosseguir para a próxima (sem pausa)

### Passo 5.3 — Atualização de MEMORY.md (única vez, ao final)

Após criar todas as stories, adicionar todas as entries ao MEMORY.md de uma única vez:
- Todas as novas stories na tabela "Pendentes"
- Se for parte de um épico, atualizar a tabela "Épicos Ativos"

**Por que ao final e não durante**: evita N leituras e escritas no MEMORY. Uma única operação é suficiente e mais econômica.

### Passo 5.4 — Relatório Final Compacto

```
✅ [N] stories criadas com sucesso

Ordem de execução:
  1. /asdlc-execute [TICKET_A] — [título]
  2. /asdlc-execute [TICKET_B] — [título] (aguarda A)
  3. /asdlc-execute [TICKET_C] — [título] (aguarda B)

Próximo passo imediato: /asdlc-execute [primeira story sem dependências]
```

> **Nada mais é perguntado ao humano** após a aprovação. O agente completa a criação autonomamente.
