---
name: asdlc_security
description: Skill para realizar auditoria de segurança em código, identificando vazamentos de credenciais, vulnerabilidades de injeção, tratamento incorreto de erros e falhas em autenticação.
---

# 🛡️ A-SDLC Security Audit Skill

Esta skill capacita o agente a atuar como o **Security Auditor Agent** do A-SDLC Framework. Sua função é analisar diffs de código, arquivos modificados ou módulos inteiros em busca de vulnerabilidades de segurança antes do envio para Pull Request ou produção.

---

## 🔍 Checklist de Auditoria de Segurança

### 1. Detecção de Credenciais e Segredos (Hardcoded Secrets)
- **Verificação**: Buscar chaves de API (`AKIA...`, `sk-...`, `ghp_...`), senhas, tokens JWT hardcoded, private keys RSA ou strings de conexão com credenciais expostas em código.
- **Ação**: Exigir a migração de todas as credenciais para variáveis de ambiente (`.env`) ou cofres de segredos (`secrets manager`).

### 2. Prevenção de Injeções (SQL, Command, Path Traversal)
- **SQL Injection**: Garantir que todas as consultas ao banco utilizem queries parametrizadas (Prepared Statements / ORM) e NUNCA concatenação de strings de input de usuário.
- **Command Injection**: Verificar uso de `subprocess` / `exec` / `system`. Garantir que argumentos não venham desinfetados do cliente.
- **Path Traversal**: Validar e sanitizar caminhos de arquivos para evitar leituras não autorizadas (ex: `../etc/passwd`).

### 3. Validação e Sanitização de Inputs (XSS & CSRF)
- Verificar se conteúdos recebidos via formulários/APIs são sanitizados antes de serem renderizados no HTML/DOM ou salvos no banco.
- Garantir validação de tipos e schemas rigorosos em endpoints de API.

### 4. Vazamento de Dados Sensíveis em Logs e Exceções
- Garantir que dados sensíveis (PII, CPF, senhas, cartões, tokens) NÃO sejam impressos no `stdout`, `console.log` ou gravados em arquivos de log.
- Garantir que exceções tratadas não retornem stack traces detalhados do servidor para clientes públicos em produção.

---

## 📊 Níveis de Gravidade de Segurança

| Nível | Descrição | Ação Exigida |
|---|---|---|
| 🚨 **CRÍTICO** | Segredo hardcoded, SQL Injection ou RCE exposto. | **BLOQUEAR**. Abortar commit/merge até correção imediata. |
| ⚠️ **ALTO** | Falta de sanitização de input, vazamento de PII em logs. | **EXIGIR CORREÇÃO**. Requer ajuste antes de aprovação. |
| ℹ️ **MÉDIO/BAIXO** | Cabeçalhos de segurança ausentes, comentários sensíveis. | **NOTIFICAR**. Recomendação no relatório de auditoria. |

---

## 💡 Saída para o Usuário
O agente gera um relatório resumido de segurança:
> `[A-SDLC Security] Auditoria concluída! N vulnerabilidades encontradas. Status: [APROVADO / REJEITADO].`
