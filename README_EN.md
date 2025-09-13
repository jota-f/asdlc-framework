# 🚀 A-SDLC Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![A-SDLC Compliant](https://img.shields.io/badge/A--SDLC-Compliant-brightgreen.svg)](https://github.com/jota-f/asdlc-framework)

**Revolutionary framework for software development with specialized AI agents**, focused on high speed, high quality, and a structured process based on well-defined personas.

> **Attention:** This project is 100% free, non-commercial, no donations, no crowdfunding, no financial rewards, and no charges of any kind. All contact must be made exclusively via GitHub (issues, discussions, PRs).

## 🧠 What is A-SDLC?

**A-SDLC (AI-Driven Software Development Lifecycle)** is an innovative framework that integrates **specialized AI agents** into the software development lifecycle, not just as coding tools, but as **active participants** in a structured and managed process.

### **📚 Fundamental Concepts:**

#### **1. 🤖 Specialized Agents with Personas:**
The framework uses 5 agents with well-defined responsibilities:

- **Code Agent** 💻 - Senior Full-Stack Developer
  - Implementation of clean and efficient code
  - Following patterns and best practices
  - Inline documentation and modular structuring

- **Test Agent** 🧪 - Senior QA Engineer  
  - Creation of comprehensive tests (unit, integration, e2e)
  - Validation of acceptance criteria
  - Edge case coverage

- **Architecture Agent** 🏗️ - Senior Software Architect
  - Definition of architecture and technologies
  - Design patterns and scalability
  - Strategic technical decision making

- **Requirements Agent** 📋 - Senior Requirements Analyst
  - Elicitation and analysis of requirements
  - Definition of acceptance criteria
  - Technical and functional documentation

- **Review Agent** 👀 - Senior Code Reviewer
  - Code review and quality
  - Security and performance verification
  - Compliance with established standards

#### **2. 📝 Intelligent Plan Generation:**
The main innovation is the **generation of detailed execution plans** for each "story", which guide the developer (and their AI assistants) through a checklist of best practices, from requirements analysis to implementation, testing, and documentation.

#### **3. 🏗️ Standardized Structure:**
Each A-SDLC project follows a consistent structure:

```
my-project/
├── PROJECT_CONTEXT.md     # Complete technical context
├── .asdlc/
│   └── agents/           # Personas of the 5 specialized agents
├── stories/              # Detailed feature planning
├── prompts/              # Templates for external LLMs
└── src/                  # Project source code
```

## ✨ Features

- **🔄 Hybrid Architecture:** Use via CLI for automation or via Interactive Menu for discovery
- **🧠 Plan Generator:** Create "stories" that transform into detailed execution plans in Markdown
- **🤖 Specialized Agents:** 5 well-defined personas for different aspects of development
- **📚 Professional Prompts:** Optimized templates for use with ChatGPT, Gemini, and other LLMs
- **⚡ Smart CLI:** Modern interface with real-time validation and feedback
- **🎯 Automatic Compliance:** Guarantee that projects follow A-SDLC standards

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jota-f/asdlc-framework.git
   cd asdlc-framework
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit the .env file and add your OPENAI_API_KEY
   ```

## 🚀 How to Use

### **1. 🖥️ CLI Mode (Recommended)**

Ideal for automation and experienced users:

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Create a new project with specific type
python main.py --auto --choice 1 --project-name "my-api" --prompt "User management API" --project-type "web_api"

# Interactive mode to create project
python main.py
# Choose: 1 (Initialize new project)
```

### **2. 🎮 Interactive Mode**

Ideal for new users and feature exploration:

```bash
# Execute without arguments for interactive menu
python main.py
```

**Available Menu:**
- 🚀 Initialize new project
- 📁 Open existing project  
- 📝 Create/Implement Story
- 📋 List Stories
- ❌ Exit

### **3. 📁 Working with Existing Projects**

```bash
# Navigate to project directory
cd my-existing-project

# Create new story
python ../main.py
# Choose: 3 (Create/Implement Story)

# List existing stories
python ../main.py
# Choose: 4 (List Stories)
```

## 📚 A-SDLC Workflow

### **🔄 Typical Process:**

1. **📋 Initialization:** 
   - Automatic creation of A-SDLC structure
   - Generation of detailed `PROJECT_CONTEXT.md`
   - Installation of 5 specialized agents
   - Creation of prompt templates

2. **📝 Planning:**
   - Creation of stories with high-level description
   - Automatic generation of detailed plans by LLM
   - Definition of specific file manifests
   - Establishment of acceptance criteria

3. **⚡ Implementation:**
   - Use of professional prompts with external LLMs
   - Following checklists of specialized agents
   - Implementation guided by well-defined personas
   - Continuous compliance validation

4. **✅ Validation:**
   - Automatic verification of real implementation
   - Functional test validation
   - Compliance with A-SDLC standards
   - Updated documentation

## 🎯 Supported Project Types

A-SDLC adapts its plans and agents for different project types:

- **🌐 web_frontend** - Web frontend applications (HTML/CSS/JS, React, Vue)
- **🔌 web_api** - Web backend APIs (Python FastAPI, Node.js Express)
- **🌐 web_fullstack** - Complete web applications (Frontend + Backend)
- **📱 mobile** - Mobile applications (React Native, Flutter)
- **💻 desktop** - Desktop applications (Electron, Tkinter)
- **🤖 cli** - Command line applications

## 📁 File Structure

```
A-SDLC-Framework/
├── asdlc/                    # 🧠 Core framework
│   ├── project_manager.py    # Project management
│   ├── story_manager.py      # Story management
│   ├── plan_generator.py     # Plan generation with LLM
│   ├── ui_manager.py         # User interface
│   └── llm_client.py         # LLM API client
├── .asdlc/                   # 🤖 A-SDLC framework configuration
│   └── agents/               # Specialized agents
├── prompts/                  # 📚 Templates for external LLMs
├── examples/                 # 📖 Example projects
├── tests/                    # 🧪 Framework tests
├── main.py                   # 🚀 Entry point
├── PROJECT_CONTEXT.md        # 📋 Framework's own context
└── README.md                 # 📖 This documentation
```

## 🔧 Technologies

- **Python 3.8+** - Main language
- **OpenAI API** - GPT integration for plan generation
- **argparse** - Command line interface
- **PyYAML** - Configurations and metadata
- **python-dotenv** - Environment variable management

## 📖 Documentation

For more details on how to use A-SDLC:

- **📋 [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Complete technical context of the framework
- **📚 [prompts/README.md](prompts/README.md)** - How to use templates with external LLMs
- **📖 [examples/](examples/)** - Example projects implemented with A-SDLC

### 🔍 Comparison Example

To demonstrate the difference between traditional development and A-SDLC:

- **📝 [examples/No A-SDLC/](examples/No%20A-SDLC/)** - TodoList implemented without framework (for comparison)
- **📖 [examples/web_frontend/](examples/web_frontend/)** - TodoList implemented with A-SDLC

**Compare the two examples** to see how A-SDLC improves code quality, structure, and professionalism.

## 🤝 Contributing

Contributions following the A-SDLC process are welcome!

1. Fork the project
2. Create a story for your improvement using A-SDLC itself
3. Implement following the agent personas
4. Open a Pull Request with complete documentation

## 📄 License

This project is under MIT license with non-commercial use restrictions.

### 📋 Terms of Use

- **✅ Free Use:** For personal, educational, and non-commercial projects
- **❌ Commercial Use:** Prohibited without explicit authorization
- **📝 Attribution:** Required in all uses
- **🔗 Citation:** Must include reference to A-SDLC framework

### 📝 How to Attribute

When using the A-SDLC Framework, include:

```markdown
Developed with [A-SDLC Framework](https://github.com/jota-f/asdlc-framework)
```

Or in code:

```python
# Developed with A-SDLC Framework
# https://github.com/jota-f/asdlc-framework
```

### 🏢 Commercial Licensing

For commercial use, contact for specific licensing.

---

**💡 Developed following its own A-SDLC standards - A framework that practices what it teaches!** 