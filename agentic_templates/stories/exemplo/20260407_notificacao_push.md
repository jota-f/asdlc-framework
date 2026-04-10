---
title: "Sistema de Notificações Push via WebSocket"
ticket: "20260407_NOTIFY"
status: "CONCLUÍDO"
priority: "P1"
labels: ["backend", "realtime"]
depends_on: []
---

# Plano de Execução: Sistema de Notificações Push via WebSocket

## 📝 Especificações da Story

**História do Usuário:**
Como um usuário logado, eu quero receber notificações em tempo real sobre atualizações no sistema, para que eu permaneça informado sem precisar refreshar a página.

## Manifesto de Arquivos

- **CRIAR:** 
  - `src/services/websocket.ts`
  - `src/services/notification.ts`
  - `src/hooks/useWebSocket.ts`
  - `src/contexts/NotificationContext.tsx`
- **MODIFICAR:** 
  - `src/App.tsx` (adicionar Provider do NotificationContext)
  - `src/api/client.ts` (adicinar interceptador de WebSocket)

## 🎯 Tarefas Detalhadas (Code Agent)

### Tarefa 1: Criar serviço WebSocket
1. **Arquivo alvo**: `src/services/websocket.ts`
2. **Ação Técnica**: Criar classe WebSocketService com métodos connect(), disconnect(), send(). Implementar reconexão automática com exponential backoff (máx 5 tentativas).

### Tarefa 2: Criar hook useWebSocket
1. **Arquivo alvo**: `src/hooks/useWebSocket.ts`
2. **Ação Técnica**: Criar hook React que expõe estado de conexão e callbacks onMessage, onError.

### Tarefa 3: Criar NotificationContext
1. **Arquivo alvo**: `src/contexts/NotificationContext.tsx`
2. **Ação Técnica**: Criar Context com Provider que gerencia lista de notificações. Métodos: addNotification, removeNotification, clearAll.

## ✅ Critérios de Aceitação (Test Agent)

- [x] WebSocket conecta ao servidor sem erros
- [x] Mensagem recebida atualiza a lista de notificações em tempo real
- [x] Reconexão automática funciona após disconnect
- [x] Notificações persistem em localStorage
- [x] Componente exibe badge com contagem de unread notifications

## 📋 Regras Ocultas (Architecture & Review Agent)

- Usar WebSocket API nativa do navegador (não usar bibliotecas externas)
- Tratamento de erro deve propagar status HTTP apropriado
- Conexão deve ser fechada ao desmontar componente (cleanup)
- Limitar a 50 notificações em memória (FIFO para excessos)

## 🤖 Instruções Finais para o Orquestrador

- [x] Fase 1: Leia `PROJECT_CONTEXT.md` confirmando a Stack.
- [x] Fase 2: Siga o Manifesto de Arquivos estritamente.
- [x] Fase 3: Escreva e execute os Testes associados aos Critérios de Aceitação.
- [x] Fase 4: Se todos os critérios passarem, mude o frontmatter deste arquivo `status` de "PENDENTE" para "CONCLUÍDO".
