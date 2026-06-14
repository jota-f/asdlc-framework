---
description: Workflow para verificar versões, gerenciar venv e atualizar as habilidades (Skills), fluxos (Workflows) e scripts de código (Python/CLI) do A-SDLC diretamente do repositório oficial de forma automática e segura.
---

# 🔄 ATUALIZAR TEMPLATES E CLI A-SDLC (`/asdlc-update`)

Use este comando para instruir o agente de IA a verificar novas versões, gerenciar o ambiente Python (incluindo criação de virtualenv) e atualizar tanto os templates quanto o CLI de código para a versão mais recente oficial de forma segura.

---

## Passos do Workflow

### 1. VERIFICAÇÃO DE VERSÃO E COMPARAÇÃO
Antes de alterar qualquer arquivo, o agente DEVE verificar se há atualizações:
1. **Detectar Versão Local**: O agente lê a primeira linha do arquivo local `agentic_templates/README.md` (ou `README.md` da raiz) para identificar a versão atual (ex: `v2.5.0`).
2. **Clone Raso Temporário**: Executa no terminal um clone temporário e rápido do repositório oficial:
   ```bash
   git clone --depth 1 https://github.com/jota-f/asdlc-framework.git .temp_asdlc
   ```
3. **Detectar Versão Remota**: Lê a primeira linha de `.temp_asdlc/agentic_templates/README.md` para identificar a última versão disponível.
4. **Reportar ao Usuário**:
   - Se as versões forem iguais: *"Você já está na versão mais recente (X). Deseja forçar a reinstalação/atualização dos arquivos?"*
   - Se houver versão mais recente: *"Nova versão disponível: X (versão atual: Y). Iniciando atualização..."*

---

### 2. PREPARAÇÃO DO AMBIENTE PYTHON (VENV)
O agente deve verificar e preparar o ambiente de execução Python se houver código Python no projeto:
1. **Verificar Python**: Executa `python --version` ou `python3 --version` para ver se o interpretador está disponível.
   - Se o Python **não** estiver instalado, o agente alerta o usuário sobre as limitações (o CLI/Dashboard não funcionará) e prossegue apenas para a atualização dos templates (Modo Agentic Puro).
2. **Gerenciamento de Venv**: Se o Python estiver disponível:
   - Verifica se as pastas `venv/` ou `.venv/` existem no projeto.
   - Se não existirem, cria a venv automaticamente:
     ```bash
     python -m venv venv
     ```
   - Instala/atualiza as dependências necessárias no virtualenv:
     - No Windows (PowerShell):
       ```powershell
       venv\Scripts\pip install -r .temp_asdlc/requirements.txt
       ```
     - No Linux/macOS:
       ```bash
       venv/bin/pip install -r .temp_asdlc/requirements.txt
       ```

---

### 3. APLICAÇÃO CIRÚRGICA DA ATUALIZAÇÃO (COPIA SEGURA)

O agente realiza a cópia dos arquivos atualizados de `.temp_asdlc` para o projeto local com as seguintes diretrizes:

#### A. Atualização da CLI e Core Python (Se aplicável)
Se o projeto local contiver os arquivos do CLI (`main.py` ou a pasta `asdlc/` existirem), o agente DEVE atualizá-los para garantir compatibilidade com novos comandos:
- **Copiar e substituir**: a pasta `asdlc/`, o arquivo `main.py` e o `requirements.txt`.

#### B. Atualização do Modo Agentic (Templates e Lógica)
O agente atualiza os arquivos de automação da IDE:
- **Copiar e substituir**: a pasta `agentic_templates/skills/` (ou `skills/` se instalados na raiz), a pasta `agentic_templates/workflows/` (ou `workflows/`) e o validador `validate_stories.py`.
- **Copiar e substituir**: os templates genéricos em `agentic_templates/templates/` (ou `templates/`), como `story_template.md`, `bug_template.md`, `backlog_template.md` e `learning_template.md`.

#### C. LEI DE SEGURANÇA E PROTEÇÃO DE DADOS (CRÍTICO)
O agente **NUNCA** deve copiar, substituir ou alterar os seguintes arquivos locais do usuário:
- ❌ A pasta `stories/` e o arquivo `stories/MEMORY.md`.
- ❌ O arquivo `PROJECT_CONTEXT.md` na raiz do projeto.
- ❌ O arquivo `GLOSSARY.md` na raiz do projeto.
- ❌ O arquivo `BACKLOG.md` na raiz do projeto.
- ❌ Qualquer arquivo `.env` ou chaves de configuração locais.

---

### 4. LIMPEZA E VALIDAÇÃO FINAL

1. **Remover Clone Temporário**:
   - No Windows (PowerShell):
     ```powershell
     Remove-Item -Recurse -Force .temp_asdlc
     ```
   - No Linux/macOS:
     ```bash
     rm -rf .temp_asdlc
     ```
2. **Executar Validador**: O agente roda o script de validação de histórias para garantir que a estrutura continua íntegra:
   - Se venv disponível:
     - Windows: `venv\Scripts\python agentic_templates/validate_stories.py` (ou `python validate_stories.py`)
     - Linux/macOS: `venv/bin/python agentic_templates/validate_stories.py` (ou `python validate_stories.py`)
3. **Resumo das Novidades**: Exibe ao usuário a confirmação de sucesso com a nova versão ativa e uma lista das principais melhorias instaladas.

---
*A-SDLC Native Agentic Mode — Update Workflow v2.5.0 (Robust Environment & Python Core Updater)*
