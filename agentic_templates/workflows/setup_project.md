# ⚙️ INICIALIZAR REPOSÍTÓRIO A-SDLC (`/asdlc-setup`)

Este workflow realiza o **Auto-Discovery e Inicialização do Repositório**, mapeando a stack tecnológica, frameworks de teste, linter e regras de build do projeto atual para criar o arquivo de contexto do agente (`PROJECT_CONTEXT.md`).

### Passos do Workflow

1. **Ativação da Skill**:
   Ao receber o comando `/asdlc-setup`, a IA ativará a **Skill `asdlc_setup`**.

2. **Inspecção de Arquivos de Manifesto**:
   O agente lê a raiz do workspace identificando:
   - `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.
   - Presença de diretórios virtuais (`venv/`, `.venv/`, `node_modules/`).

3. **Mapeamento de Comandos Mandatórios**:
   - Identifica os comandos exatos para rodar a suíte de testes (ex: `pytest`, `npm test`, `cargo test`).
   - Identifica os comandos de linter/formatação (ex: `ruff check .`, `eslint .`).

4. **Geração do `PROJECT_CONTEXT.md`**:
   - Escreve ou atualiza o arquivo `PROJECT_CONTEXT.md` na raiz do projeto com o manifesto detectado e as convenções do A-SDLC (limite de 300 linhas por arquivo novo, TDD obrigatório, escudo anti-racionalização).

5. **Confirmação Visual**:
   - O agente apresenta um resumo dos comandos detectados e confirma que o repositório está pronto para a execução das stories via `/asdlc-execute`.
