# 🛡️ AUDITORIA DE SEGURANÇA DE CÓDIGO (`/asdlc-security`)

Este workflow é utilizado para realizar uma auditoria rigorosa de segurança em código fonte, buscando vulnerabilidades comuns (OWASP Top 10), credenciais expostas e falhas em sanitização de dados antes do envio de alterações.

### Passos do Workflow

1. **Seleção do Alvo**:
   Especifique o arquivo, diretório ou diff a ser auditado (ex: `/asdlc-security src/` ou `/asdlc-security`).

2. **Ativação da Skill**:
   A IA ativará a **Skill `asdlc_security`**.

3. **Execução do Checklist OWASP & Secret Scanning**:
   - Varredura de chaves de API, senhas e tokens hardcoded.
   - Inspeção de queries de banco em busca de SQL Injection.
   - Verificação de sanitização de inputs em rotas e formulários.
   - Inspeção de vazamentos de dados PII em logs e mensagens de erro.

4. **Classificação de Achados**:
   - O agente categoriza cada apontamento como 🚨 CRÍTICO, ⚠️ ALTO ou ℹ️ MÉDIO/BAIXO.

5. **Relatório & Recomendação**:
   - Se houver achados 🚨 CRÍTICO ou ⚠️ ALTO, o agente bloqueia o encerramento da tarefa e fornece a correção sugerida em código.
   - Se nenhuma falha grave for encontrada, o agente emite o selo `[A-SDLC Security Approved]`.
