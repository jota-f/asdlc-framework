# 📚 Guia de Stories de Exemplo

Este diretório contém exemplos de Stories A-SDLC para referência.

## 📋 Sistema de Versionamento

### Padrão de Nomeação
```
YYYYMMDD_<feature_name>.md
```

Exemplos:
- `20260407_notificacao_push.md` - Primeira feature
- `20260408_dashboard_graficos.md` - Segunda feature

### Subtarefas (Versions)

Para stories grandes, divida em partes sequenciais:

```
20260407_notificacao_push_v1.md  # Core WebSocket
20260407_notificacao_push_v2.md  # Integração com UI
20260407_notificacao_push_v3.md  # Persistência
```

## 🔗 Sistema de Dependências

### Campo `depends_on`

No frontmatter YAML, adicione o campo `depends_on`:

```yaml
---
title: "Minha Story"
ticket: "20260407_FEATURE"
status: "PENDENTE"
depends_on: ["20260406_OUTRA_FEATURE"]
---
```

### Regras de Dependência

1. **Story dependente só pode ser implementada** se todas as dependências tiverem `status: "CONCLUÍDO"`
2. **Verifique dependências automaticamente** antes de executar `/asdlc-execute`
3. **Referencie pelo ticket** (não pelo nome do arquivo)

### Exemplo de Cadeia de Dependências

```
Story A (20260401) ──────► Story B (20260402) ──────► Story C (20260403)
     CONCLUÍDO                CONCLUÍDO                  PENDENTE
```

Story C só pode ser executada após A e B estarem concluídas.

## 📝 Exemplo 1: Story Independente

[`20260407_notificacao_push.md`](./20260407_notificacao_push.md) - Sistema de notificações em tempo real

Características:
- `depends_on: []` (sem dependências)
- `status: CONCLUÍDO` (já implementada)

## 📝 Exemplo 2: Story Dependente

[`20260408_dashboard_graficos.md`](./20260408_dashboard_graficos.md) - Dashboard com gráficos

Características:
- `depends_on: ["20260407_NOTIFY"]` (depende da story de notificações)
- `status: PENDENTE` (aguarda implementação)
- Inclui verificação de dependência nas "Regras Ocultas"

## ⚡ Validação de Dependências

Antes de executar uma story, o agente deve:

1. Ler o frontmatter YAML da story alvo
2. Verificar campo `depends_on`
3. Para cada ticket em `depends_on`:
   - Buscar arquivo correspondente em `stories/`
   - Verificar se `status: "CONCLUÍDO"`
4. Se alguma dependência não estiver concluída, abortar com erro claro

## 🔄 Como Criar Subtasks

1. **Identifique o escopo**: A story é muito grande?
2. **Quebre logicamente**: Core → UI → Integração → Tests
3. **Crie versionamento**: Use sufixo `_v1`, `_v2`, etc.
4. **Mantenha dependência**: Cada versão pode depender da anterior

Exemplo:
```yaml
# Story v1 - Core
---
title: "Auth v1 - Estrutura Base"
ticket: "20260407_AUTH_V1"
status: "CONCLUÍDO"
depends_on: []
---

# Story v2 - UI  
---
title: "Auth v2 - Tela de Login"
ticket: "20260408_AUTH_V2"
status: "PENDENTE"
depends_on: ["20260407_AUTH_V1"]
---

# Story v3 - Integração
---
title: "Auth v3 - Backend API"
ticket: "20260409_AUTH_V3"
status: "PENDENTE"
depends_on: ["20260408_AUTH_V2"]
---
```
