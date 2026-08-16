---
name: asdlc_tdd
description: Skill de desenvolvimento orientado a testes (TDD). Executa o ciclo estrito Red-Green-Refactor, garantindo que nenhum código de produção seja escrito sem um teste falhando correspondente.
user_command: /tdd
invocation_mode: user_and_model
tags: [tdd, testing, quality, red-green-refactor, unit-tests]
---

# 🔴🟢🔵 A-SDLC TDD Cycle Skill (`/tdd`)

Esta skill aplica a disciplina de Test-Driven Development (TDD) rigorosa para garantir código testável, resiliente e livre de regressões.

---

## 🔁 O Ciclo Red-Green-Refactor

```
      [ 1. RED ]  ------->  Escreva um teste que falha para o comportamento desejado
          |
          v
     [ 2. GREEN ] ------->  Escreva o MÍNIMO de código necessário para o teste passar
          |
          v
    [ 3. REFACTOR ] ----->  Limpe e otimize o código mantendo todos os testes verdes
```

---

## 🧭 Procedimento de Execução

### Passo 1: 🔴 RED (Escrever Teste Falhando)
1. Localize a suíte de testes correspondente (ex: `tests/test_feature.py` ou `src/__tests__/feature.test.ts`).
2. Crie um caso de teste que verifica exatamente a nova regra de negócio ou edge case.
3. **Execute o comando de teste** no terminal (ex: `pytest tests/test_feature.py` ou `npm test`).
4. **Confirme que o teste FALHOU** e que a mensagem de falha é exatamente a esperada (ex: `AttributeError`, `AssertionError`).
   - *Se o teste já passar antes de implementar, o teste está incorreto ou a funcionalidade já existia!*

### Passo 2: 🟢 GREEN (Fazer o Teste Passar)
1. Escreva **apenas** o código estritamente necessário para que o teste passe.
2. Evite abstrações prematuras nesta fase; foque em fazer a asserção ficar verde.
3. Execute novamente o comando de teste.
4. **Confirme que todos os testes passaram (100% GREEN)**.

### Passo 3: 🔵 REFACTOR (Refatorar com Segurança)
1. Analise o código recém-escrito:
   - Remova duplicações de lógica.
   - Melhore a legibilidade e nomes de variáveis de acordo com `GLOSSARY.md`.
   - Garanta que a complexidade ciclomática esteja baixa.
2. Execute a suíte de testes novamente para garantir que nenhuma regressão foi introduzida.

---

## ⚠️ Regras Inegociáveis do Agente
- **NUNCA** implemente a lógica de produção antes de ver o teste falhar.
- **NUNCA** marque uma tarefa como concluída se os testes estiverem com skip ou falhas.
- Isole dependências externas (banco, APIs) usando Mocks/Stubs apenas quando necessário; prefira testes em memória.
