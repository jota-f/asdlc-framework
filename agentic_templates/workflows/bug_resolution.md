# 🐛 Workflow de Resolução de Bugs (A-SDLC)

Este workflow deve ser seguido rigorosamente quando o comando `/asdlc-bug` for invocado ou um erro for identificado.

## 🚀 Ciclo de Vida do Bug

### Fase 1: Triagem e Diagnóstico (Triagem)
**Ação:** Coletar evidências e entender o rastro do erro.
1.  Leia o `PROJECT_CONTEXT.md` e a `MEMORY.md`.
2.  Busque por logs (`.log`), stack traces no terminal ou mensagens de erro.
3.  Identifique em quais arquivos e linhas o erro ocorre.
4.  Considere commits ou mudanças recentes.

### Fase 2: Reprodução (Reprodução)
**Ação:** Criar um teste que falha.
1.  Crie um novo arquivo de teste (ex: `tests/reproduction/test_issue_XYZ.py`).
2.  Simule o cenário exato onde o bug acontece.
3.  Execute o teste: ele **DEVE FALHAR**.
4.  Se o teste passar, você ainda não reproduziu o bug. Ajuste o teste.

### Fase 3: Análise de Causa Raiz (RCA)
**Ação:** Isolar a falha técnica.
1.  Use o "Bug Hunter Skill" para encontrar a linha e a lógica falha.
2.  Determine se é um erro de lógica, um edge case não tratado ou uma regressão.
3.  Documente a RCA internamente antes de corrigir.

### Fase 4: Planejamento e Fix (Correção)
**Ação:** Criar a Bug Story e aplicar o fix.
1.  Use o `templates/bug_template.md` para criar uma story em `stories/`.
2.  Referencie o teste de reprodução como critério de aceitação #1.
3.  Execute o fix conforme planejado.

### Fase 5: Validação e Regressão (Validação)
**Ação:** Garantir que o fix resolveu tudo.
1.  Role o teste de reprodução: agora deve **PASSAR**.
2.  Role a suite de testes completa: NADA deve ter quebrado (Regressão).
3.  Atualize a `MEMORY.md` com a lição aprendida ("Bug X resolvido em arquivo Y").
4.  Marque a story como `CONCLUÍDO`.

---
*A-SDLC Native Agentic Mode - Workflow v1.0*
