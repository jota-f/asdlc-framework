# 🌌 A-SDLC Framework (v2.2.0)
**AI-Driven Software Development Lifecycle**

A-SDLC is a software engineering framework designed to transform AIs into autonomous agents capable of managing the full project lifecycle. It utilizes **Harness Engineering**, **Recursive Handoffs**, and **Feedback Loops** to ensure high-fidelity code.

---

## 📍 Table of Contents
- [🚀 What is A-SDLC?](#-what-is-a-sdlc)
- [⚙️ Installation and Setup](#️-installation-and-setup)
- [🧠 MCP Mode (Antigravity Power)](#-mcp-mode-antigravity-power)
- [🛠️ Agentic Mode (IDE Templates)](#️-agentic-mode-ide-templates)
- [🏃 How to Get Started (Workflow)](#-how-to-get-started-workflow)
- [📂 Recommended Workspace Structure](#-recommended-workspace-structure)
- [📖 Examples and Use Cases](#-examples-and-use-cases)
- [📄 Terms of Use](#-terms-of-use)

---

## 🚀 What is A-SDLC?
Unlike simple chat assistants, A-SDLC treats AI as a **Multi-Agent System (MAS)**. Every task passes through specialists (Requirements, Architecture, Code, Testing) who validate each other's work through a "Harness" that monitors errors in real-time.

---

## ⚙️ Installation and Setup

### 1. Requirements
- Python 3.10+
- Git

### 2. Cloning and Dependencies
```bash
git clone https://github.com/jota-f/A-SDLC.git
cd A-SDLC
pip install -r requirements.txt
cp .env.example .env
```

---

## 🧠 MCP Mode (Antigravity Power)
This is the most advanced mode. It connects the framework directly to your IDE (Cursor/Windsurf) via the **Model Context Protocol**, allowing the framework to use the IDE's intelligence without needing external API keys.

### How to install the MCP server:
1. **Install libraries**: `pip install fastmcp mcp`
2. **Configure your IDE**: Add the server to your `mcp_config.json` file:
```json
"asdlc": {
  "command": "python",
  "args": ["C:/Path/To/A-SDLC/asdlc/mcp_server.py"],
  "env": { "PYTHONPATH": "C:/Path/To/A-SDLC" }
}
```
3. **Restart the IDE**. Now I (Antigravity) will have native A-SDLC "tools" to create projects and stories for you!

---

## 🛠️ Agentic Mode (IDE Templates)
If you don't want to use the Python Engine and prefer to work only in the IDE chat:
1. Copy the `agentic_templates/` folder to your project root.
2. Use `@asdlc-plan.md` to plan and `@asdlc-coder.md` to code.
3. [See Detailed Guide here](agentic_templates/README_EN.md).

---

## 🏃 How to Get Started (Workflow)

### Scenario A: New Project
```bash
python main.py create-project --name "my_new_app" --prompt "App description"
```

### Scenario B: Existing Project (Integration)
```bash
python main.py create-project --name "my_project" --path "C:/path/to/project" --prompt "Analysis"
```

---

## 📂 Recommended Workspace Structure
To avoid confusion between framework files and your project code, we recommend:
```text
C:/Dev/
  ├── A-SDLC/             <-- Central Framework
  ├── Project_Alpha/      <-- Your project (with .asdlc and stories installed)
  └── Project_Beta/       <-- Another project
```

---

## 📖 Examples and Use Cases

### 🚗 Drowsiness Sensor (Arduino/ESP32)
A real example of how A-SDLC can be used in embedded systems.
- **Location**: `test_projects/drowsinessSensor`
- **Highlight**: Use of feedback sensors to validate firmware compilation.

### 📝 Fullstack TodoList
Classic example to understand the flow from requirements to E2E testing.
- **Location**: `examples/web_fullstack`

---

## 📄 Terms of Use
This framework is under MIT license with a restriction: **Commercial use is prohibited without authorization**.
- **Free**: Personal, academic, and open-source use.
- **Attribution**: Mandatory to cite "Developed with A-SDLC Framework".

---
**💡 A-SDLC: Where code isn't just written, it's engineered by machines and validated by rules.**