# 🌌 A-SDLC Framework (v2.4.0)
**AI-Driven Software Development Lifecycle**

A-SDLC is a framework that turns AI assistants into autonomous agents capable of managing the full software development lifecycle. It uses **Harness Engineering**, **Mandatory TDD**, **Tracer Bullets**, and **Feedback Loops** to ensure high-fidelity code.

---

## Table of Contents

- [What is A-SDLC?](#what-is-a-sdlc)
- [Three Ways to Use](#three-ways-to-use)
- [Installation](#installation)
- [Antigravity Mode (Free)](#antigravity-mode-free)
- [External API Mode (Autonomous)](#external-api-mode-autonomous)
- [Agentic Mode (No Python) - RECOMMENDED](agentic_templates/README_EN.md)
- [Complete Workflow](#complete-workflow)
- [CLI Commands](#cli-commands)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Key Concepts](#key-concepts)
- [Examples](#examples)
- [Terms of Use](#terms-of-use)

---

## What is A-SDLC?

Unlike chat assistants, A-SDLC treats AI as a **Multi-Agent System (MAS)**. Each task is executed by specialist agents (Requirements, Architecture, Code, Testing, Review) who validate each other's work.

### Framework Pillars

| Pillar | Description |
|--------|-------------|
| **Harness Engineering** | Each agent operates in an isolated environment with lean context and validation sensors |
| **Mandatory TDD** | Tests are created BEFORE code (Red → Green → Refactor) |
| **Tracer Bullets** | Tasks cross all layers (DB → API → UI) for immediate feedback |
| **Smart Zone** | Context monitoring to keep LLM in the precision zone (<80k tokens) |
| **Recursive Handoffs** | Agents delegate subtasks via `[DELEGATE: type | task]` |

---

## Three Ways to Use

| | 🧠 Antigravity (IDE) | ⚡ External API (CLI) | 📋 [Agentic (Templates)](agentic_templates/README_EN.md) |
|---|---|---|---|
| **Who thinks?** | The IDE (Cursor/Windsurf) | OpenAI/OpenRouter API | The IDE (chat) |
| **Cost** | Free | Paid (tokens) | Free |
| **Complexity** | Medium (MCP server) | Low (CLI) | Minimal (copy/paste) |
| **Autonomy** | Semi-autonomous | 100% autonomous | Semi-autonomous |
| **Best for** | Large projects | Full automation | Quick prototyping |

---

## Installation

### Requirements
- Python 3.10+
- Git

### Step 1: Clone and install dependencies
```bash
git clone https://github.com/jota-f/A-SDLC.git
cd A-SDLC
pip install -r requirements.txt
```

### Step 2: Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` according to the mode you want to use (see below).

### Step 3 (Optional): Configure MCP for IDE
```bash
pip install fastmcp mcp
```
Add to your IDE's `mcp_config.json`:
```json
"asdlc": {
  "command": "python",
  "args": ["C:/Path/To/A-SDLC/asdlc/mcp_server.py"],
  "env": { "PYTHONPATH": "C:/Path/To/A-SDLC" }
}
```

---

## Antigravity Mode (Free)

In this mode, the IDE is the "brain." MCP serves as a management tool.

### Configuration
```env
ASDLC_ENGINE=antigravity
```

### Available MCP Tools
| Tool | Function |
|------|----------|
| `asdlc_create_project` | Initialize a project |
| `asdlc_create_story` | Create a story |
| `asdlc_get_story_details` | Read story content |
| `asdlc_update_story_status` | Update status |
| `asdlc_list_stories` | List stories |
| `asdlc_get_project_metrics` | Progress metrics |
| `asdlc_validate_project` | Validate compliance |

### How to implement
In the IDE chat:
> *"Use the @asdlc_implementation skill to implement story @stories/ID"*

---

## External API Mode (Autonomous)

The Python script takes full control, using OpenAI/OpenRouter API to spawn autonomous agents.

### Configuration
```env
ASDLC_ENGINE=external
OPENROUTER_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
```

### Additional MCP Tools
| Tool | Function |
|------|----------|
| `asdlc_implement_story` | Autonomous execution via agents |
| `asdlc_spawn_specialist` | Invoke ad-hoc agent |

### How to implement
```bash
python main.py implement --id 20260425_204837
```

---

## Agentic Mode (No Python)

> [!TIP]
> **RECOMMENDED MODE FOR CURSOR/WINDSURF:** This mode does not require Python or CLI installation. It injects A-SDLC "intelligence" directly into your IDE chat via templates.

### 📥 Quick Installation
Copy the templates folder to your project:
```bash
cp -r agentic_templates/ your-project/
```
*(Optional: Rename `agentic_templates/` to `.agents/` for native compatibility with some IDEs).*

### 🚀 Available Chat Commands
| Command | What it does |
|---------|--------------|
| `/asdlc-grill` | "Grills" you on requirements to avoid vague demands. |
| `/asdlc-architecture` | Starts technical discussion and domain modeling. |
| `/asdlc-create-story` | Creates a formal story following framework standards. |
| `/asdlc-execute` | Implements the story using the **Mandatory TDD** cycle. |

### 📖 Detailed Guide
For a complete guide on how to configure skills and workflows in your IDE, see:
👉 **[Agentic Mode Guide (README in agentic_templates)](agentic_templates/README_EN.md)**

---

## Complete Workflow

### Scenario A: New Project
```bash
python main.py create-project --name "my_app" --prompt "App description"
```

### Scenario B: Existing Project
```bash
python main.py create-project --name "my_project" --path "C:/path/to/project" --prompt "Analysis"
```

### Scenario C: Create Story
```bash
python main.py create-story --title "Implement Login"
```

### Scenario D: Implement Story (TDD)
```bash
python main.py implement --id 20260504_120000_implement_login
```

### Scenario E: List Stories
```bash
python main.py list-stories
```

### Scenario F: Validate Project
```bash
python main.py validate --format markdown
```

---

## CLI Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `create-project` | Initialize new project | `--name`, `--prompt`, `--type`, `--path` |
| `create-story` | Create a story | `--title` |
| `implement` | Run TDD implementation | `--id` |
| `list-stories` | List all stories | — |
| `validate` | Validate compliance | `--project`, `--format`, `--output` |

### Interactive mode (no arguments)
```bash
python main.py
```
Displays an interactive menu with all options.

---

## Environment Variables

### Required
| Variable | Description |
|----------|-------------|
| `ASDLC_ENGINE` | `antigravity` (default) or `external` |
| `OPENROUTER_API_KEY` | OpenRouter key (when `external`) |
| `OPENAI_API_KEY` | OpenAI key (when `external`, fallback) |

### Optional (external mode)
| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_MODEL` | `gpt-4.1-mini` | Default model |
| `OPENAI_MAX_TOKENS` | `4096` | Token limit |
| `OPENAI_TEMPERATURE` | `0.3` | Temperature |
| `MODEL_CODE` | — | Model for Code Agent |
| `MODEL_ARCH` | — | Model for Architecture Agent |
| `MODEL_TEST` | — | Model for Test Agent |
| `MODEL_REQ` | — | Model for Requirements Agent |
| `MODEL_REVIEW` | — | Model for Review Agent |

---

## Project Structure

```
my-project/
├── .asdlc/
│   ├── agents/              # 6 agent personas
│   │   ├── code_agent.md
│   │   ├── test_agent.md
│   │   ├── architecture_agent.md
│   │   ├── requirements_agent.md
│   │   ├── review_agent.md
│   │   └── bug_hunter_agent.md
│   └── harness/             # Agent output (runtime)
├── stories/                 # Stories + MEMORY.md
│   └── MEMORY.md
├── prompts/                 # LLM prompt templates
├── PROJECT_CONTEXT.md       # Project blueprint
├── BACKLOG.md               # Technical debt (auto-generated)
└── src/                     # Project code
```

---

## Key Concepts

### TDD Pipeline (Mandatory)
```
Architecture → Test Red → Code Green → Validation → Review
```
- **Red**: Tests are created and FAIL (executable specification)
- **Green**: Code is implemented until tests pass
- **Refactor**: Code improvement with tests as safety net

### Smart Zone vs Dumb Zone
| Zone | Tokens | Behavior |
|------|--------|----------|
| Smart Zone | < 80k | LLM is precise |
| Warning | 80k-100k | Quality degrades |
| Dumb Zone | > 100k | LLM makes silly errors |

### Tracer Bullets (Vertical Slices)
```
CORRECT: Model + Endpoint + Test (one story)
WRONG: All models → All endpoints → All tests
```

### Inviolable Law
**NEVER** mark a story as DONE without a `run_command` returning exit code 0.

---

## Examples

### 🚗 Drowsiness Sensor (Arduino/ESP32)
- **Location**: `test_projects/drowsinessSensor`
- Feedback sensors to validate firmware compilation

### 📝 Fullstack TodoList
- **Location**: `examples/web_fullstack`
- Complete flow from requirements to E2E testing

---

## Terms of Use

MIT license with restriction: **Commercial use prohibited without authorization**.
- **Free**: Personal, academic, and open-source use
- **Attribution**: Mandatory to cite "Developed with A-SDLC Framework"

---

**A-SDLC: Where code isn't just written, it's engineered by machines and validated by rules.**
