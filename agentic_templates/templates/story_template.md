---
title: "[TÍTULO PEQUENO]"
ticket: "[YYYYMMDD_HASH]"
status: "PENDENTE"
priority: "P1|P2|P3"
labels: ["", ""]
depends_on: []
---

# Plano de Execução: [TÍTULO]

## 📝 Especificações da Story
**História do Usuário:**
Como um [ATOR], eu quero [AÇÃO], para que [BENEFÍCIO].

## Manifesto de Arquivos
- **CRIAR:** [arquivos novos - ex: `src/components/Button.tsx`]
- **MODIFICAR:** [arquivos existentes - ex: `src/utils/math.ts`]

## 🎯 Tarefas Detalhadas

### Tarefa 1: [Nome]
1. **Arquivo**: [caminho]
2. **Ação**: [o que fazer]

### Tarefa N: ...

## ✅ Critérios de Aceitação (Test Agent)
- [ ] Critério testável 1
- [ ] Critério testável 2

## 📋 Regras Ocultas
- Usar padrões do `PROJECT_CONTEXT.md`
- Tratamentos de erro propagam status codes
- **Filosofia Ponytail / YAGNI**: Priorizar soluções nativas e a solução mais simples/curta que funcione, evitando abstrações extras.
- **Limites de Código**: Novos arquivos no máximo 300 linhas; sem inchaço em arquivos legados gigantes (>1500 linhas) — extrair para novos arquivos.

## 🧪 Teste
Identifique o sistema de teste usado: npm test, pytest, cargo test, go test, etc.

## 🤖 Instruções Finais
- [ ] Fase 1: Leia PROJECT_CONTEXT (seção relevante)
- [ ] Fase 2: Verifique depends_on (todas CONCLUÍDAS)
- [ ] Fase 3: Siga Manifesto estritamente (Priorizando simplicidade e menor diff)
- [ ] Fase 4: Execute testes + lint/typecheck
- [ ] Fase 5: Mude status → CONCLUÍDO

---
*Template de Story do A-SDLC Framework*
