---
name: asdlc_setup
description: Skill para inicialização e auto-discovery do repositório, configurando PROJECT_CONTEXT.md, test runners e linters.
user_command: /setup-asdlc
invocation_mode: user_and_model
tags: [setup, init, discovery, project-context, bootstrap]
---

# 🚀 A-SDLC Setup & Discovery Skill

Esta skill atua como o **Repo Discovery Agent** do A-SDLC Framework. Sua função é inspecionar um repositório existente ou novo, identificar suas tecnologias, comandos de teste, linter e convenções, gerando ou atualizando o arquivo de contexto do projeto (`.asdlc/PROJECT_CONTEXT.md` ou `PROJECT_CONTEXT.md`).

---

## 🔍 Processo de Inspecção e Auto-Discovery

O agente executa uma varredura ordenada na raiz do repositório:

### 1. Detecção de Linguagem e Gerenciador de Pacotes
- **Node.js / TypeScript / JavaScript**: Presença de `package.json`. Identificar gerenciador: `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun), `package-lock.json` (npm).
- **Python**: Presença de `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `poetry.lock`. Identificar se há venv em `venv/` ou `.venv/`.
- **Rust**: Presença de `Cargo.toml`.
- **Go**: Presença de `go.mod`.
- **Java / Kotlin**: Presença de `pom.xml` (Maven) ou `build.gradle` / `build.gradle.kts` (Gradle).
- **C# / .NET**: Presença de arquivos `.csproj` ou `.sln`.

### 2. Detecção do Test Runner (Crucial)
- **Node/TS**: Inspecionar a seção `"scripts"` do `package.json` por `test`, `vitest`, `jest`, `mocha`, `playwright`.
- **Python**: Checar dependências para `pytest`, `unittest`. Comando padrão: `pytest` ou `python -m unittest`.
- **Rust**: Comando padrão `cargo test`.
- **Go**: Comando padrão `go test ./...`.
- **Java**: `mvn test` ou `./gradlew test`.

### 3. Detecção de Linter e Formatador
- **Node/TS**: Inspecionar por `eslint`, `prettier`, `biome`.
- **Python**: Inspecionar por `ruff`, `flake8`, `black`, `mypy`.
- **Rust**: `cargo clippy`, `cargo fmt`.
- **Go**: `golangci-lint`, `go fmt`.

---

## 📋 Ação de Geração do Contexto (`PROJECT_CONTEXT.md`)

Após a varredura, o agente cria ou atualiza o arquivo `PROJECT_CONTEXT.md` (ou `.asdlc/PROJECT_CONTEXT.md`) com a estrutura padronizada:

```markdown
# 🗺️ Project Context: [Nome do Projeto]

## 🛠️ Tecnologias & Tooling Detectados
- **Linguagem Principal**: [ex: Python / TypeScript]
- **Gerenciador de Dependências**: [ex: npm / poetry / venv]
- **Suíte de Testes**: [ex: pytest / vitest]
- **Linter / Formatador**: [ex: ruff / eslint]

## ⚡ Comandos Mandatórios
- **Executar Testes**: `[ex: venv/Scripts/pytest ou npm test]`
- **Executar Linter**: `[ex: ruff check . ou npm run lint]`
- **Build**: `[ex: npm run build ou cargo build]`

## 📏 Convenções do Repositório
- **Tamanho Máximo de Arquivos Novos**: 300 linhas.
- **TDD Obrigatório**: Testes automatizados DEVEM falhar antes de passar.
- **Evidência Obrigatória**: O status `CONCLUÍDO` só pode ser atribuído após exit code 0 nos testes.
```

---

## 💡 Saída para o Usuário
O agente resume os achados em uma resposta clara:
> `[A-SDLC Setup] Projeto inspecionado com sucesso! Contexto gerado em PROJECT_CONTEXT.md com a suíte de testes '[COMANDO]' configurada.`
