# 🤖 A-SDLC Agentic Mode Guide (v2.4.0)

## What is this directory?

A-SDLC Agentic Mode is a way to use the framework directly inside your IDE (Cursor, Windsurf, Cline, RooCode) **without needing Python**. The methodology is injected directly into the AI agent.

Instead of running a CLI to generate markdowns and then feeding them to an AI, **you copy the templates to your project and use commands in the IDE chat**.

---

## 📥 How to Install

1. Go to your project
2. Copy the `agentic_templates/` folder to the project root
3. (Optional) Rename to `.agents/` if your IDE supports it

```bash
cp -r agentic_templates/ your-project/
```

**Result:**
```
your-project/
├── skills/                  # A-SDLC skills
├── workflows/               # Command workflows
├── stories/                 # Your stories
├── TOOL_GUIDE.md            # Token optimization guide
├── validate_stories.py      # Story validator
└── src/                     # Your code
```

---

## 🚀 Quick Start

### Available commands

| Command | When to Use |
|---------|-------------|
| `/asdlc-grill` | Guided questioning for vague requirements |
| `/asdlc-architecture` | Architecture and modeling questions |
| `/asdlc-plan` | Analyze large scope, break into stories |
| `/asdlc-create-story` | Create a formal story |
| `/asdlc-execute` | Implement a story (mandatory TDD) |
| `/asdlc-bug` | Diagnose and fix bugs |

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
- Story only executes if all dependencies = `COMPLETED`
- Agent verifies automatically before implementing

---

## 🆕 What's New (v2.3.0)

| Feature | Description |
|---------|-------------|
| `/asdlc-grill` | Proactive questioning for vague demands |
| Mandatory TDD | Pipeline: Red → Green → Refactor |
| Tracer Bullets | Vertical slices (DB → API → UI) |
| Smart Zone | Context monitoring (80k/100k tokens) |
| Deep Modules | Architecture guidance (simple interfaces) |
| `/asdlc-bug` | Bug resolution workflow with RCA |
| `asdlc_bug_hunter` | Diagnosis and root cause skill |

---

## 📁 File Structure

```
agentic_templates/
├── README.md                    # This file (EN)
├── README_EN.md                 # English version
├── TOOL_GUIDE.md               # Token optimization guide
├── validate_stories.py         # Story structure validator
├── skills/
│   ├── asdlc_story_generator/  # Requirements Agent - create stories
│   ├── asdlc_implementation/   # Code Agent - implement (TDD)
│   ├── asdlc_context_compactor/# Compact long context
│   └── asdlc_bug_hunter/       # Bug Hunter - diagnosis and RCA
├── workflows/
│   ├── grill_requirements.md   # Guided questioning
│   ├── architecture_discovery.md # Architecture discovery
│   ├── scope_analysis.md       # Scope analysis
│   ├── create_asdlc_story.md   # Story creation
│   ├── implement_asdlc_story.md # TDD implementation
│   └── bug_resolution.md       # Bug resolution
├── templates/
│   ├── story_template.md       # Standard story template
│   ├── bug_template.md         # Standard bug template
│   └── exemplo/                # Story examples
└── stories/
    └── MEMORY.md               # Project memory
```

---

## ⚡ Token Optimization

### Tips
1. **Read MEMORY.md first** - overview without iterating all stories
2. **PROJECT_CONTEXT** - include only relevant section
3. **Context Compactor** - invoke after 30+ messages
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
