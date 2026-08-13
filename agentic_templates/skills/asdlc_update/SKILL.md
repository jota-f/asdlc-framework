---
name: asdlc_update
description: Skill para verificar novas versões, gerenciar venv e atualizar as habilidades (Skills), fluxos (Workflows) e scripts do A-SDLC com segurança sem sobrescrever dados do usuário.
---

# 🔄 A-SDLC Update & Migration Skill

Esta skill capacita o agente a atuar como o **System Maintenance & Update Agent** do A-SDLC Framework, responsável por verificar novas versões no repositório oficial, sincronizar skills, workflows e CLI de código, além de preparar o ambiente Python (venv) de forma totalmente segura.

---

## 🧭 Procedimento Interno de Atualização

### 1. Detecção de Versão e Comparação
1. **Versão Local**: Lê a versão registrada em `agentic_templates/README.md` ou `README.md` (ex: `v2.7.0`).
2. **Clone Raso Temporário**: Executa no terminal:
   ```bash
   git clone --depth 1 https://github.com/jota-f/A-SDLC.git .temp_asdlc
   ```
3. **Versão Remota**: Lê a versão remota em `.temp_asdlc/agentic_templates/README.md`.
4. Se já estiver atualizado e o usuário não forçou reinstall, finaliza avisando o usuário.

### 2. Preparação do Virtualenv (Python venv)
1. Verifica se `python` / `python3` está disponível.
2. Se existirem `venv/` ou `.venv/`, utiliza-as. Se não existirem e o Python estiver disponível, cria a venv: `python -m venv venv`.
3. Instala dependências atualizadas:
   - Windows: `venv\Scripts\pip install -r .temp_asdlc/requirements.txt`
   - Linux/macOS: `venv/bin/pip install -r .temp_asdlc/requirements.txt`

### 3. Cópia Segura (Preservação de Dados do Usuário)
1. **Copiar e Atualizar**:
   - `agentic_templates/skills/` (ou `skills/`)
   - `agentic_templates/workflows/` (ou `workflows/`)
   - `agentic_templates/templates/` (ou `templates/`)
   - `agentic_templates/validate_stories.py`
   - `asdlc/`, `main.py`, `requirements.txt` (se o CLI local existir)

2. **PROIBIDO Sobrescrever (Arquivos Protegidos)**:
   - ❌ `stories/` e `stories/MEMORY.md`
   - ❌ `PROJECT_CONTEXT.md` ou `.asdlc/PROJECT_CONTEXT.md`
   - ❌ `GLOSSARY.md` e `BACKLOG.md`
   - ❌ Arquivos `.env` e configurações de ambiente locais

### 4. Limpeza e Validação
1. Remove a pasta temporária:
   - Windows: `Remove-Item -Recurse -Force .temp_asdlc`
   - Linux/macOS: `rm -rf .temp_asdlc`
2. Valida o ambiente executando `validate_stories.py`.

---

## 💡 Saída para o Usuário
> `[A-SDLC Update] Framework atualizado com sucesso para a versão v2.7.0! Skills e workflows sincronizados.`
