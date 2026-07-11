---
description: Workflow para auditar, alinhar e atualizar toda a documentação necessária do projeto (README, CHANGELOG, BACKLOG, manuais operacionais e afins) de forma dinâmica e inteligente.
---

# 📚 ATUALIZAR DOCUMENTAÇÃO (`/asdlc-doc-update`)

Use este comando sempre que concluir uma story, implementar uma refatoração importante ou corrigir um bug estrutural, instruindo o agente a auditar e atualizar os arquivos de documentação do repositório atual.

## Como Usar

No chat da IDE, execute o comando:
```
Você: /asdlc-doc-update
```
Ou passe o contexto da tarefa recém-concluída:
```
Você: /asdlc-doc-update após concluir a story de integração com a API de Pagamentos
```

---

## Passos do Workflow

### Passo 1: Descoberta e Auditoria de Documentos (MANDATÓRIO)
1. O agente varre a estrutura do repositório atual em busca de arquivos de documentação (como `README.md`, `CHANGELOG.md`, `BACKLOG.md`, `GLOSSARY.md`, manuais operacionais em pastas como `docs/`, `wiki/`, `.agents/`, etc.).
2. O agente analisa o histórico recente de modificações no código-fonte para mapear o impacto técnico das mudanças nas APIs, bancos de dados, regras de negócio ou fluxos de interface.

### Passo 2: Alinhamento e Atualização
1. O agente ativa a **Skill `asdlc_documentation_updater`**.
2. **Atualização do Glossário (se houver)**: Insere novos termos de domínio ou regras biomecânicas/comerciais identificadas no código.
3. **Atualização de Setup & Build**: Se houve adição de dependências, novas variáveis de ambiente ou novos scripts de teste, atualiza o manual correspondente (como `README.md` ou guia de onboarding).
4. **Atualização de Versão (Changelog)**: Registra a nova alteração categorizada em seu histórico público (`CHANGELOG.md` ou equivalente).
5. **Atualização de Backlog e Status**: Atualiza listagens de tarefas, marcos de desenvolvimento ou arquivos de controle (como `MEMORY.md`, `BACKLOG.md` ou `ROADMAP.md`).
6. **Atualização de Guias Visuais / UX**: Se telas foram adicionadas ou fluxos foram alterados, sincroniza manuais de design periféricos.

### Passo 3: Relatório de Atualizações
O agente exibe um resumo compacto de quais arquivos de documentação foram modificados e as razões das atualizações.
