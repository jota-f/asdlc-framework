# 🤖 A-SDLC Agentic Mode Guide (v2.6.1)

## What is this directory?

A-SDLC Agentic Mode is a way to use the framework directly inside your IDE (Cursor, Windsurf, Cline, RooCode) **without needing Python**. The methodology is injected directly into the AI agent.

Instead of running a CLI to generate markdowns and then feeding them to an AI, **you copy the templates to your project and use commands in the IDE chat**.

---

## 📥 How to Install

> [!IMPORTANT]
> **Most commands (`/asdlc-grill`, `/asdlc-create-story`, `/asdlc-execute`, etc.) require no Python.** They are purely text-based templates interpreted by the AI agent.
>
> **Exception: `/asdlc-dashboard`** — this command generates an interactive HTML file and requires `main.py` (full Python framework).

### Without Python (recommended for most users)

Copy only the templates folder to your project:
```bash
cp -r agentic_templates/ your-project/
```
*(Optional) Rename to `.agents/` if your IDE supports it.*

### With Python (required only for `/asdlc-dashboard`)

Clone the full repository:
```bash
git clone https://github.com/jota-f/asdlc-framework.git
cd asdlc-framework
pip install -r requirements.txt
```
Or copy the templates and the core Python files:
```
your-project/
├── agentic_templates/   ← templates (no Python needed)
├── asdlc/               ← Python core (only for dashboard)
├── main.py              ← CLI entry point
└── requirements.txt     ← framework dependencies
```
*If you copy manually, don't forget to run `pip install -r requirements.txt` to install the CLI dependencies.*

---

## 🚀 Quick Start

### Available commands

| Command | When to Use |
|---------|-------------|
| `/asdlc-grill` | Guided questioning for vague requirements — includes automatic Scope Gate |
| `/asdlc-architecture` | Architecture and modeling questions |
| `/asdlc-plan` | Analyze large scope, break into stories (tracer bullets) |
| `/asdlc-create-epic` | Create an Epic for high-level roadmap goals (multi-sprint) |
| `/asdlc-create-story` | Create a formal story |
| `/asdlc-execute` | Implement a story (mandatory TDD) |
| `/asdlc-bug` | Diagnose and fix bugs |
| `/asdlc-dashboard` | Generate visual project dashboard (KPIs, Kanban, Burndown, Epics) |
| `/asdlc-doc-update` | Audits and updates documentation in any project adaptively |
| `/asdlc-update` | Safely updates A-SDLC skills and workflows |

---

## 📋 Complete Workflow

### Phase 1: Requirements Validation (if vague)
> **You:** `/asdlc-grill I want to add caching to the system`

The agent questions: who uses it? which endpoint? what metric? etc.

### Phase 2: Architecture Discovery (optional)
> **You:** `/asdlc-architecture WebSocket or Server-Sent Events for notifications?`

The agent discusses options and recommends the best approach.

### Phase 3: Planning (for large features)
> **You:** `/asdlc-plan I need complete auth: login, registration, recovery, OAuth`

The agent breaks into multiple sequential stories.

### Phase 4: Story Creation
> **You:** `/asdlc-create-story WebSocket notification system`

The agent creates the story in `stories/` following the A-SDLC template.

### Phase 5: Implementation (TDD)
> **You:** `/asdlc-execute`

The agent runs the complete cycle:
1. Checks dependencies
2. Creates tests that FAIL (Red Phase)
3. Implements code until tests pass (Green Phase)
4. Validates acceptance criteria
5. Marks story as COMPLETED

### Phase 6: Visual Dashboard (optional)
> **You:** `/asdlc-dashboard`

> [!WARNING]
> This command requires the full Python framework (`main.py` + `asdlc/` folder).
> If you only copied the templates folder, the agent will generate a **text summary** of the metrics directly in the chat instead of the interactive HTML.

**With Python installed** — the agent runs `python main.py dashboard --no-open` and generates:
- `.asdlc/dashboard/dashboard.html` with KPIs, Kanban, Burndown and Velocity charts
- Opens automatically in the browser

**Without Python (templates only)** — the agent reads the stories and reports in chat:
- KPIs: total stories, completed, pending
- Stories blocked by unmet dependencies
- Stories missing acceptance criteria

> [!TIP]
> The generated HTML is self-contained. Open in any browser with no installation. Can be shared via e-mail or Slack.

---

## 🔗 Dependency System

Stories can have dependencies via the `depends_on` field:

```yaml
---
title: "Dashboard with Charts"
ticket: "20260408_DASH"
status: "PENDING"
depends_on: ["20260407_NOTIFY"]
---
```

**Rules:**
- A story will only pass validation and execute if all of its listed dependencies in the `depends_on` field are marked as **`CONCLUÍDO`** or **`Done`**. If any dependency is still `PENDENTE`, `In Progress` or any other intermediate status, the validator will return an error.
- The frontmatter parser is robust and supports both inline flow lists (e.g. `["DEP1"]`) and block lists (block sequences):
  ```yaml
  depends_on:
    - "20260407_NOTIFY"
  ```
- The story validator automatically checks these dependencies and statuses before starting any implementation.

---

## 🆕 What's New (v2.6.0)

| Feature | Description |
|---------|-------------|
| **Scope Intelligence Gate** | Automatic Story/Large Story/Epic classification built into `/asdlc-grill` and `/asdlc-create-story` |
| **Epics (`/asdlc-create-epic`)** | Native support for Epics as independent artifacts in `stories/epics/` with strategic goals and child stories |
| **MCP: `asdlc_create_epic`** | Create epics via the Model Context Protocol |
| **MCP: `asdlc_list_epics`** | List epics with calculated progress (token-efficient) |
| **Autonomous Loop in `/asdlc-plan`** | After a single approval, creates all stories sequentially, validates depends_on acyclic graphs, and updates MEMORY at once |
| **Persistent Context Handoff** | Context Compactor saves checkpoints in `.asdlc/context_checkpoint.md`. Agents read (Hot Start) and delete it automatically upon starting workflows |
| **Self-Healing Compaction** | Code/Architecture agents auto-trigger compaction and guide you to start a fresh session if they detect Dumb Zone or degradation |

---

## 🆕 What's New (v2.5.0)

| Feature | Description |
|---------|-------------|
| `/asdlc-dashboard` | Interactive visual project dashboard (KPIs, Kanban, Burndown) |
| `asdlc_dashboard` | Skill to generate and interpret the dashboard in agentic mode |
| `templates/` | Dedicated folder for templates and examples (separate from active stories) |
| `/asdlc-grill` | Proactive questioning for vague demands |
| Mandatory TDD | Pipeline: Red → Green → Refactor |
| Tracer Bullets | Vertical slices (DB → API → UI) |
| Smart Zone | Context monitoring (80k/100k tokens) |
| Deep Modules | Architecture guidance (simple interfaces) |
| `/asdlc-bug` | Bug resolution workflow with RCA |
| `asdlc_bug_hunter` | Diagnosis and root cause skill |
| Centralized Backlog | Use of `BACKLOG.md` for developer mental notes and AI technical debt |

---

## 📁 File Structure

agentic_templates/
├── README.md                    # This file (PT)
├── README_EN.md                 # English version
├── TOOL_GUIDE.md               # Token optimization guide
├── validate_stories.py         # Story structure validator
├── skills/
│   ├── asdlc_story_generator/  # Requirements Agent - create stories
│   ├── asdlc_implementation/   # Code Agent - implement (TDD)
│   ├── asdlc_context_compactor/# Compact long context (Persistent Checkpoint)
│   ├── asdlc_bug_hunter/       # Bug Hunter - diagnosis and RCA
│   ├── asdlc_dashboard/        # Visual project dashboard
│   └── asdlc_documentation_updater/ # Analyzes and updates project documentation adaptively  ← NEW
├── workflows/
│   ├── grill_requirements.md   # Guided questioning + Scope Gate
│   ├── architecture_discovery.md # Architecture discovery + Hot Start Checkpoint
│   ├── scope_analysis.md       # Scope analysis + autonomous loop
│   ├── create_epic.md          # Create strategic Epics          ← NEW
│   ├── create_asdlc_story.md   # Story creation + Scope Gate     ← UPDATED
│   ├── implement_asdlc_story.md # TDD implementation + Hot Start Checkpoint
│   ├── update_documentation.md # Audit and update documentation  ← NEW
│   ├── bug_resolution.md       # Bug resolution
│   └── dashboard.md            # Visual project dashboard
├── templates/
│   ├── story_template.md       # Standard story template
│   ├── bug_template.md         # Standard bug template
│   ├── learning_template.md    # ADRs Index (Learnings) template
│   ├── backlog_template.md     # Backlog template
│   └── exemplo/                # Story examples
└── stories/
    ├── MEMORY.md               # Project memory (stories + epics)
    └── epics/                  # Project Epics                  ← NEW
        └── EPIC_*.md           # Strategic Epic files
```

---

## ⚡ Token Optimization

### Tips
1. **Read MEMORY.md, LEARNING.md, and BACKLOG.md first** - lean overview of progress, architectural decisions, and pending ideas without scanning all stories or ADRs.
2. **PROJECT_CONTEXT** - include only relevant section
3. **Context Checkpointing** - use the compactor to save your state. In a new chat session, agents will automatically ingest the checkpoint and delete it (Hot Start).
4. **Smart Zone** - keep context < 80k tokens

### Smart Zone vs Dumb Zone
| Zone | Tokens | Behavior |
|------|--------|----------|
| Smart | < 80k | LLM is precise |
| Warning | 80k-100k | Quality degrades |
| Dumb | > 100k | LLM makes silly errors |

---

## ⚙️ Requirements

- IDE with AI agent support (Cursor, Windsurf, Cline, RooCode)
- `.agents/` folder or equivalent (optional)
- **No Python or dependencies required**

---

## 📖 More Information

- **[TOOL_GUIDE.md](TOOL_GUIDE.md)** - Tools and tokens optimization
- **[stories/MEMORY.md](stories/MEMORY.md)** - Project memory
- **[templates/exemplo/README.md](templates/exemplo/README.md)** - Versioning guide
