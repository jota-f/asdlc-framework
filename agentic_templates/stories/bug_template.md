---
title: "BUG: [Resumo Curto do Erro]"
ticket: "YYYYMMDD_BUG_ID"
status: "PENDENTE"
type: "bug_fix"
priority: "High" # High, Medium, Low
---

# 🔍 Bug Report & Fix Plan: [Nome do Bug]

## 1. Descrição do Comportamento
**Comportamento Atual:**
[Descreva o que está acontecendo de errado]

**Comportamento Esperado:**
[Descreva o que deveria acontecer]

## 2. Análise de Causa Raiz (RCA)
- **Diagnóstico**: [Por que o erro acontece?]
- **Localização**: [Arquivo.py:Linha]

## 3. Manifesto de Reprodução
- **Teste de Regressão**: `[Caminho do Arquivo de Teste]`
- **Comando de Reprodução**: `pytest [Caminho do Teste]`

## 4. Manifesto de Arquivos
- **CRIAR**:
  - `[Novo arquivo de teste de regressão]`
- **MODIFICAR**:
  - `[Arquivo onde o fix será aplicado]`

## 5. Tarefas de Correção
- [ ] Criar teste de regressão que reproduz a falha.
- [ ] Validar a falha no teste criado.
- [ ] Aplicar correção no arquivo `[Nome]`.
- [ ] Validar se o teste de regressão passa agora.
- [ ] Executar suite de testes completa para garantir não-regressão.

## ✅ Critérios de Aceitação
- [ ] Teste de regressão `[Nome]` passa com sucesso.
- [ ] Suite de testes original continua passando (100% pass).
- [ ] [Outro critério específico se houver]

---
*Template de Bug do A-SDLC Framework*
