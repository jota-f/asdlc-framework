---
name: asdlc_bug_hunter
description: Skill para triagem de bugs, análise de causa raiz (RCA) e reprodução obrigatória via testes automatizados.
user_command: /triage-bug
invocation_mode: user_and_model
tags: [bug, triage, rca, debugging, reproduction, tests]
---

# 🕵️‍♂️ Skill: A-SDLC Bug Hunter

Esta skill capacita o agente a realizar diagnósticos profundos e resoluções seguras de bugs seguindo a metodologia A-SDLC.

## 🧭 Quando Usar
- Quando o usuário reportar um comportamento inesperado ("Bug").
- Quando um teste automatizado falhar sem motivo aparente.
- Quando for necessário realizar um Root Cause Analysis (RCA).

## 🛠️ Procedimento Interno (Mental Model)

### 1. Fase de Isolamento (Triage)
Antes de olhar o código, entenda o contexto:
- Quais arquivos foram alterados recentemente?
- O erro é determinístico (acontece sempre) ou intermitente?
- Peça logs, stack traces ou screenshots se não estiverem disponíveis.

### 2. Fase de Reprodução (Obrigatória)
**NUNCA tente corrigir um bug que você não conseguiu reproduzir com um teste.**
- Crie um arquivo de teste específico para o bug (ex: `tests/reproduce_issue_XYZ.py`).
- O teste deve FALHAR com o erro relatado.
- Se você não consegue criar um teste que falhe, você ainda não entendeu o bug.

### 3. Root Cause Analysis (J-Space Cognitive Step)
Use a técnica dos "5 Porquês" e deliberação interna antes de tocar no código:
- **Hipótese**: Por que a falha ocorreu? (Rastreie a origem exata dos dados)
- **Deliberação**: A correção proposta altera o comportamento esperado de outras partes do sistema?
- **Identifique o arquivo e a linha exata.**
- **Patch Cirúrgico**: Planeje a menor alteração suficiente para sanar o defeito sem introduzir mocks desnecessários.

### 4. Ciclo de Fix A-SDLC
1. **Prepare a Story**: Use `/asdlc-bug` ou crie uma story manual com `type: bug_fix`.
2. **Manenha a MESMA story até resolver**: NAO crie novas stories para o mesmo bug. Se descobrir que a correção não resolve completamente, CONTINUE na mesma story - adicione tarefas extras ate resolver.
3. **Implemente o Fix**: Foque exclusivamente em resolver a causa raiz.
4. **Valide a Regressão**:
    - O teste de reprodução agora PASSA?
    - A suite de testes completa continua PASSANDO?

## 🛡️ Escudo Anti-Racionalização (Anti-Lazy Shield)
- **PROIBIDO "Symptom Patching"**: Não insira `try/except` silenciosos, fallbacks nulos ou mocks artificiais apenas para fazer o erro desaparecer sem entender a causa raiz.
- **PROIBIDO desativar testes falhando**: Nunca comente ou remova asserções quebradas para alegar que o bug foi resolvido.
- **REQUISITO DE EVIDÊNCIA**: Só declare o bug como resolvido após o teste de reprodução e a suíte completa de testes retornarem `exit code 0` no terminal.

## 🚫 Anti-Patterns (O que NÃO fazer)
- **"Shotgun Debugging"**: Mudar várias coisas aleatoriamente esperando que o erro suma.
- **"Symptom Fixing"**: Colocar um `if obj is not None` para esconder um erro, em vez de descobrir por que ele é None.
- **Ignorar Regressão**: Corrigir o bug A e quebrar a funcionalidade B por falta de testes de integração.

## 💡 Comandos Rápidos (Mente do Agente)
- `/asdlc-bug [descrição do erro]` -> Inicia o workflow de resolução.

---
*A-SDLC Native Agentic Mode - Skill v1.0*
