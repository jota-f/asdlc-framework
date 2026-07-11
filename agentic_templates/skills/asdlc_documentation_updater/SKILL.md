---
name: asdlc_documentation_updater
description: Skill do framework A-SDLC para analisar, descobrir e atualizar a documentação de qualquer projeto (README, CHANGELOG, BACKLOG, manuais e afins) de forma dinâmica e adaptável ao repositório.
---

# 📚 A-SDLC Documentation Updater Skill

Esta skill orienta o agente a auditar, descobrir e atualizar os documentos de qualquer projeto após a conclusão de tarefas, garantindo consistência técnica, atualização de guias e alinhamento de terminologias de forma inteligente e adaptável a cada repositório.

---

## 🔍 Descoberta Dinâmica de Documentação (MANDATÓRIO)

Antes de realizar qualquer alteração nos arquivos de documentação, o agente deve executar uma fase de **descoberta ativa** no repositório em que está trabalhando. Cada projeto possui sua própria estrutura de documentação.

### O agente DEVE varrer o projeto procurando por:
1. **Padrões de Nome na Raiz**: `README.md`, `README_*.md`, `CHANGELOG.md`, `GLOSSARY.md`, `BACKLOG.md`, `CONTRIBUTING.md`.
2. **Diretórios de Documentação**: Pastas como `docs/`, `doc/`, `wiki/`, `documentation/`, `.agents/`, `.github/`.
3. **Manuais de Domínio Específicos**: Arquivos markdown que tratam de guias de arquitetura, fluxos de interface (UX), guias de API, diagramas ou manuais operacionais.

*Se o repositório possuir arquivos ou diretórios específicos que não constam na hierarquia padrão abaixo, o agente deve listá-los e decidir de forma autônoma quais deles precisam de atualização de acordo com a modificação realizada no código.*

---

## 🛠️ A Hierarquia Adaptável de Documentos

Ao atualizar a documentação, o agente deve respeitar a finalidade de cada arquivo encontrado no repositório:

1. **Glossário / Linguagem Ubíqua (ex: `GLOSSARY.md` ou similar):**
   * *Propósito:* O dicionário central de termos de negócio e conceitos do sistema.
   * *Regra:* Atualize sempre que a alteração introduzir novos termos de domínio ou alterar significados de conceitos existentes.
2. **Decisões de Arquitetura (ex: `docs/adr/`, `LEARNING.md` ou similar):**
   * *Propósito:* Registro histórico de decisões de arquitetura e trade-offs técnicos.
   * *Regra:* Registre novas decisões estruturais importantes na seção de ADRs existente no repositório.
3. **Mapeamento de Tarefas e Backlog (ex: `MEMORY.md`, `BACKLOG.md` ou similar):**
   * *Propósito:* Acompanhamento do progresso de tarefas e listagem de débitos técnicos gerados.
   * *Regra:* Marque tarefas como concluídas, mova tickets se aplicável e adicione eventuais débitos técnicos identificados durante a execução do código.
4. ** README principal (ex: `README.md`):**
   * *Propósito:* O ponto de entrada principal e apresentação do repositório.
   * *Regra:* Atualize guias de build, comandos de teste, requisitos ou seções de status de fases caso a mudança afete o setup do projeto ou as conquistas da milestone atual.
5. **Histórico de Alterações (ex: `CHANGELOG.md`):**
   * *Propósito:* O histórico de versões público (preferencialmente seguindo o padrão *Keep a Changelog*).
   * *Regra:* Registre as novas alterações sob as categorias apropriadas (`Adicionado`, `Modificado`, `Corrigido`, `Removido`).
6. **Manuais Periféricos e Guias de UX/API:**
   * *Propósito:* Detalhes visuais, de navegação de telas, contratos de rotas API ou fluxogramas.
   * *Regra:* Mantenha estes manuais sincronizados caso rotas HTTP, fluxos de telas ou comportamentos de interface de usuário tenham sido alterados no código.

---

## 🔄 Fluxo de Trabalho do Agente

### Passo 1: Auditoria e Mapeamento de Necessidades
1. Execute uma busca rápida para identificar quais arquivos de documentação estão presentes no repositório atual.
2. Faça uma avaliação crítica: a mudança no código-fonte altera a API, os requisitos, o processo de setup, ou introduz novos conceitos de domínio?
3. Se sim, mapeie quais arquivos identificados no passo 1 sofrerão impacto.

### Passo 2: Alinhamento de Terminologia e Domínio
1. Caso novos termos tenham sido inseridos, documente a definição no arquivo de glossário/dicionário do repositório para evitar inconsistências no futuro.

### Passo 3: Atualização de Guias Operacionais e Setup
1. Se a alteração adicionou uma nova variável de ambiente (no `.env`), alterou dependências (como `package.json`, `requirements.txt`, `Cargo.toml`) ou modificou o fluxo de execução/testes:
   - Atualize os guias de setup e as instruções de teste no `README.md` ou nos manuais equivalentes.

### Passo 4: Fechamento de Status (Backlog/Histórico)
1. Atualize a versão e as modificações feitas no arquivo de controle de versão (`CHANGELOG.md` ou correspondente).
2. Se houver controle de backlog ou pendências em disco (como `BACKLOG.md` ou `MEMORY.md`), dê baixa nas pendências concluídas e adicione novas notas ou melhorias planejadas.
