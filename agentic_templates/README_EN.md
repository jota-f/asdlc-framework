# 🤖 A-SDLC Agentic Mode Guide

## What is this directory?
The A-SDLC Native Agentic Mode is an alternative way to use the A-SDLC framework, specifically designed for developers who already use local autonomous AI Assistants (such as MCP extensions, Cline, Cursor, Windsurf, RooCode).

Instead of you (human) running a Python CLI to generate static markdowns and then feeding them to an AI, **this architecture injects the A-SDLC methodology directly into the mind of your AI Agent**. No middlemen.

## 📥 How to Install in Any Project

You don't need to add the A-SDLC Python package. You just need to instill the "behavior" into your repository:

1. Go to your project target project.
2. Ensure the base structure for agent guidelines is there (e.g., the `.agents/` folder supported by AI Software Engineering tools).
3. **Copy the `skills/` and `workflows/` folders from this repository to your setup.**

**The result should look like this:**
```bash
your-existing-app/
├── .agents/
│   ├── skills/
│   │   ├── asdlc_story_generator/
│   │   └── asdlc_implementation/
│   └── workflows/
│       ├── create_asdlc_story.md
│       └── implement_asdlc_story.md
├── src/ 
└── stories/
```

## 🚀 Daily Usage

Open your favorite IDE's chat. Don't create huge prompts from scratch. Invoke the instances you now have on your machine!

### Phase 1: Architecture-Based Story Creation (Product Owner)
> **You:** `/asdlc-create-story I need push notification logic based on WebSockets`

The local assistant will invoke the instruction. It will actively scan the `src/` folder, read `PROJECT_CONTEXT.md` (if you have one), format the request as a detailed file-based specification (Standard A-SDLC), and automatically create the `.md` file in the `stories/` folder for your approval.

### Phase 2: Actual Implementation and Testing (Dev, Test & Reviewer)
With the created story markdown, and after you (human) read and adjust it, you command:
> **You:** `/asdlc-execute`

The assistant will open the backlog. The `asdlc_implementation` skill will force it to transition its cognition:
1. **Act as Architect:** Reading the contract instead of just coding whatever comes to mind.
2. **Act as Code Agent:** Applying code injections strictly where the manifest authorizes.
3. **Act as Test Agent:** Calling commands in the host terminal unseen by you until the "passed" flag shines.
4. It will change the "status" key from PENDING to COMPLETED in the story.

## 💡 Case Study: Creating something from Scratch

How do you use A-SDLC when you **don't even know how to code** a complex feature yet? A-SDLC is not just for generating code, but for helping you structure and design the application.

Imagine you want to add a financial "Invoice" structure linked to "Orders" in your E-Commerce.

### 1. Invoke the "Architecture Agent" (Discovery Phase)
Before creating an official Story, clear up the modeling doubts by interacting freely with your local AI:
> **You:** *"Act as the A-SDLC Architecture Agent. I want to add the 'Invoice' entity to the app. I have 'Order' and 'Item', but I don't know the proper database hierarchy. Give me design options and recommend the best structure."*

The AI will analyze your domain and suggest the correct table modeling and dependencies (e.g., "Create an `Invoices` table with a foreign key to `Orders`"). You discuss the modeling until reaching a solid consensus.

### 2. Invoke the Workflow (Turning the idea into a Plan)
Once the architecture is decided in the conversation, the doubt is gone. You invoke the tactical formatting:
> **You:** *"/asdlc-create-story Now that we decided the architecture, act as Requirements Agent. Create the Story to implement the 'invoices' table in the database and connect it to 'orders'."*

**Result:** A-SDLC will take that "free talk" and freeze it into a rigid manifest inside `stories/2026xxxx_feature_invoices.md`. The Story will list exactly which files will be created (e.g., `src/models/invoice.py`) and modified.

### 3. Automated Implementation (Code Agent & Test Agent)
Only after you visually approve this Story, you command:
> **You:** *"/asdlc-execute"*

And the Code Agent and Test Agent will invisibly program over your files strictly what was methodically signed in the plan, running terminal tests and only stopping when the status changes from "PENDING" to "COMPLETED".

## Advantages
- **Agnostic:** Works perfectly in React, Python, Kotlin, Rust. The framework helps you manage the Agents.
- **Fast:** You skip the Python setup. Just copy and paste `.agents/`.
- **Personal Traceability:** A-SDLC lets you see the exact implementation plan before an Agent destroys your repository with unwanted edits.
