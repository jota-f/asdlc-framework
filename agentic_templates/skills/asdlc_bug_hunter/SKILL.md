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

### 3. Root Cause Analysis (RCA)
Use a técnica dos "5 Porquês" internamente:
- Por que a variável estava nula? (Porque a função X retornou None)
- Por que a função X retornou None? (Porque o DB estava offline)
- ...e assim por diante.
- **Identifique o arquivo e a linha exata.**

### 4. Ciclo de Fix A-SDLC
1. **Prepare a Story**: Use `/asdlc-bug` ou crie uma story manual com `type: bug_fix`.
2. **Manenha a MESMA story até resolver**: NAO crie novas stories para o mesmo bug. Se descobrir que a correção não resolve completamente, CONTINUE na mesma story - adicione tarefas extras ate resolver.
3. **Implemente o Fix**: Foque exclusivamente em resolver a causa raiz.
4. **Valide a Regressão**:
    - O teste de reprodução agora PASSA?
    - A suite de testes completa continua PASSANDO?

## 🚫 Anti-Patterns (O que NÃO fazer)
- **"Shotgun Debugging"**: Mudar várias coisas aleatoriamente esperando que o erro suma.
- **"Symptom Fixing"**: Colocar um `if obj is not None` para esconder um erro, em vez de descobrir por que ele é None.
- **Ignorar Regressão**: Corrigir o bug A e quebrar a funcionalidade B por falta de testes de integração.

## 💡 Comandos Rápidos (Mente do Agente)
- `/asdlc-bug [descrição do erro]` -> Inicia o workflow de resolução.

---
*A-SDLC Native Agentic Mode - Skill v1.0*
