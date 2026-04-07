# 🤖 A-SDLC Agentic Mode Guide (v2.0.0)

## What is this directory?
A-SDLC Native Agentic Mode is an alternative way to use the A-SDLC framework, specifically designed for developers who already use local autonomous AI Assistants (such as MCP extensions, Cline, Cursor, Windsurf, RooCode).

Instead of you (human) running a Python CLI to generate static markdowns and then feeding them to an AI, **this architecture injects the A-SDLC methodology directly into the mind of your AI Agent**. No middlemen.

## 📥 How to Install in Any Project

You don't need to add the A-SDLC Python package. Just install the "behavior" into your repository:

1. Go to your target project.
2. Ensure the base structure for agent guidelines is there (e.g., the `.agents/` folder supported by AI Software Engineering tools).
3. **Copy the `agentic_templates/` folder from this repository to your project root.**
4. Rename to `.agents/` if your tool supports it (optional).

**The result should look like this:**
```bash
your-project/
├── .agents/              # (optional - rename agentic_templates/)
│   ├── skills/
│   ├── workflows/
│   └── stories/
├── src/
└── stories/              # Your generated stories
```

---

## 🚀 Quick Start

### Step 1: Copy the folder
```bash
cp -r agentic_templates/ your-project/
```

### Step 2: Done! Use commands in IDE chat

| Command | When to Use |
|---------|-------------|
| `/asdlc-architecture` | Architecture and modeling questions (before creating story) |
| `/asdlc-plan` | Analyze large scope and break into multiple stories |
| `/asdlc-create-story` | Create a formal story after defining context |
| `/asdlc-execute` | Execute/implement a pending story |

---

## 📋 Complete Workflow

### Phase 1: Discovery (Optional)
> **You:** `/asdlc-architecture I want to add WebSocket for notifications. WebSocket or Server-Sent Events?`

The agent acts as Architecture Agent, discusses options, and recommends the best approach. No files created yet.

### Phase 2: Planning (Optional)
> **You:** `/asdlc-plan I need complete auth: login, registration, password recovery, OAuthGoogle`

The agent analyzes the scope and creates multiple sequential stories if needed:
- Auth v1: Core + Database
- Auth v2: UI (Login/Registration)
- Auth v3: API Endpoints
- Auth v4: OAuth

### Phase 3: Story Creation
> **You:** `/asdlc-create-story WebSocket notification system`

The agent creates the story in `stories/` following the A-SDLC template.

### Phase 4: Implementation
> **You:** `/asdlc-execute`

The agent executes the story: creates files, runs tests, marks as COMPLETED, and updates the index.

---

## 🆕 What's New (v2.0.0)

| Feature | Description |
|---------|------------|
| `/asdlc-architecture` | Architectural discovery workflow |
| `/asdlc-plan` | Scope analysis with automatic break into sub-stories |
| `depends_on` | Dependency system between stories |
| `MEMORY.md` | Consolidated project memory (optimizes tokens) |
| `Context Compactor` | Skill to reduce tokens in long sessions |
| `TOOL_GUIDE.md` | Tool optimization guide |

---

## 🔗 Dependency System

Stories can have dependencies. Use the `depends_on` field:

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
- Agent verifies automatically
- Reference by ticket

---

## 📊 Story Versioning

For large features, split into parts:

```
YYYYMMDD_feature_v1.md  # Core
YYYYMMDD_feature_v2.md  # UI  
YYYYMMDD_feature_v3.md  # Integration
```

Recommended split: Core → UI → Integration → Tests

---

## ⚡ Token Optimization

Agentic Mode automatically minimizes tokens:

### Context Structure

| Element | % of Context |
|---------|-------------|
| System prompt | 1-2.5% |
| Tool definitions | 1.5-5% |
| Few-shot | 1-4% |
| Current story | 25% |
| History | 50% |

### Tips

1. **Read MEMORY.md first** - overview without iterating stories
2. **PROJECT_CONTEXT** - include only relevant section
3. **Context Compactor** - invoke after 30+ messages
4. **Local cache** - store project conventions

---

## 📁 File Structure

```
agentic_templates/
├── README.md                    # This file
├── README_EN.md                 # English version
├── TOOL_GUIDE.md               # Optimization guide
├── validate_stories.py         # Story validator
├── skills/
│   ├── asdlc_story_generator/  # Create stories
│   ├── asdlc_implementation/  # Execute stories
│   └── asdlc_context_compactor/ # Compact context
├── workflows/
│   ├── architecture_discovery.md
│   ├── scope_analysis.md
│   ├── create_asdlc_story.md
│   └── implement_asdlc_story.md
└── stories/
    ├── MEMORY.md                # Project memory
    └── exemplo/                 # Examples
```

---

## 💡 Usage Tips

### Always read first:
```bash
stories/MEMORY.md  # ~200 tokens vs 5000+ of all stories
```

### For architecture questions:
```
/asdlc-architecture What's the best approach for auth in React + Node?
```

### For large scopes:
```
/asdlc-plan I need a complete e-commerce system
```

---

## ⚙️ Requirements

- IDE with AI agent support (Cursor, Windsurf, Cline, RooCode)
- `.agents/` folder or equivalent supported by IDE
- No Python or dependencies required

---

## 📖 More Information

- **[stories/exemplo/README.md](stories/exemplo/README.md)** - Complete versioning guide
- **[TOOL_GUIDE.md](TOOL_GUIDE.md)** - Tools and tokens optimization
- **[stories/MEMORY.md](stories/MEMORY.md)** - Project memory (auto-generated)
