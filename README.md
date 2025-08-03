# 🚀 A-SDLC Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![A-SDLC Compliant](https://img.shields.io/badge/A--SDLC-Compliant-brightgreen.svg)](https://github.com/jota-f/asdlc-framework)

**Framework revolucionário para desenvolvimento de software com agentes de IA especializados**, focado em alta velocidade, alta qualidade e um processo estruturado baseado em personas bem definidas.

> **Atenção:** Este projeto é 100% gratuito, não comercial, sem doações, sem crowdfunding, sem recompensas financeiras e sem qualquer tipo de cobrança. Todo contato deve ser feito exclusivamente via GitHub (issues, discussions, PRs).

## 🧠 O que é o A-SDLC?

**A-SDLC (AI-Driven Software Development Lifecycle)** é um framework inovador que integra **agentes de IA especializados** no ciclo de vida de desenvolvimento de software, não apenas como ferramentas de codificação, mas como **participantes ativos** de um processo estruturado e gerenciado.

### **📚 Conceitos Fundamentais:**

#### **1. 🤖 Agentes Especializados com Personas:**
O framework utiliza 5 agentes com responsabilidades bem definidas:

- **Code Agent** 💻 - Desenvolvedor Sênior Full-Stack
  - Implementação de código limpo e eficiente
  - Seguimento de padrões e boas práticas
  - Documentação inline e estruturação modular

- **Test Agent** 🧪 - QA Engineer Sênior  
  - Criação de testes abrangentes (unitários, integração, e2e)
  - Validação de critérios de aceitação
  - Cobertura de casos edge

- **Architecture Agent** 🏗️ - Arquiteto de Software Sênior
  - Definição de arquitetura e tecnologias
  - Padrões de design e escalabilidade
  - Tomada de decisões técnicas estratégicas

- **Requirements Agent** 📋 - Analista de Requisitos Sênior
  - Elicitação e análise de requisitos
  - Definição de critérios de aceitação
  - Documentação técnica e funcional

- **Review Agent** 👀 - Code Reviewer Sênior
  - Revisão de código e qualidade
  - Verificação de segurança e performance
  - Conformidade com padrões estabelecidos

#### **2. 📝 Geração Inteligente de Planos:**
A principal inovação é a **geração de planos de execução detalhados** para cada "story", que guiam o desenvolvedor (e seus assistentes de IA) através de um checklist de melhores práticas, desde a análise de requisitos até a implementação, testes e documentação.

#### **3. 🏗️ Estrutura Padronizada:**
Cada projeto A-SDLC segue uma estrutura consistente:

```
meu-projeto/
├── PROJECT_CONTEXT.md     # Contexto técnico completo
├── .asdlc/
│   └── agents/           # Personas dos 5 agentes especializados
├── stories/              # Planejamento detalhado de funcionalidades
├── prompts/              # Templates para LLMs externas
└── src/                  # Código fonte do projeto
```

## ✨ Features

- **🔄 Arquitetura Híbrida:** Use via CLI para automação ou via Menu Interativo para descoberta
- **🧠 Plan Generator:** Crie "stories" que se transformam em planos de execução detalhados em Markdown
- **🤖 Agentes Especializados:** 5 personas bem definidas para diferentes aspectos do desenvolvimento
- **📚 Prompts Profissionais:** Templates otimizados para usar com ChatGPT, Gemini e outras LLMs
- **⚡ CLI Inteligente:** Interface moderna com validação e feedback em tempo real
- **🎯 Conformidade Automática:** Garantia de que projetos sigam padrões A-SDLC

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone [URL-DO-SEU-REPOSITORIO]
   cd asdlc-framework
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua API key da OpenAI:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e adicione sua OPENAI_API_KEY
   ```

## 🚀 Como Usar

### **1. 🖥️ Modo CLI (Recomendado)**

Ideal para automação e usuários experientes:

```bash
# Ativar ambiente virtual
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Criar um novo projeto com tipo específico
python main.py --auto --choice 1 --project-name "minha-api" --prompt "API de gestão de usuários" --project-type "web_api"

# Modo interativo para criar projeto
python main.py
# Escolha: 1 (Inicializar novo projeto)
```

### **2. 🎮 Modo Interativo**

Ideal para novos usuários e exploração das funcionalidades:

```bash
# Execute sem argumentos para menu interativo
python main.py
```

**Menu disponível:**
- 🚀 Inicializar novo projeto
- 📁 Abrir projeto existente  
- 📝 Criar/Implementar Story
- 📋 Listar Stories
- ❌ Sair

### **3. 📁 Trabalhando com Projetos Existentes**

```bash
# Navegar para diretório do projeto
cd meu-projeto-existente

# Criar nova story
python ../main.py
# Escolha: 3 (Criar/Implementar Story)

# Listar stories existentes
python ../main.py
# Escolha: 4 (Listar Stories)
```

## 📚 Workflow A-SDLC

### **🔄 Processo Típico:**

1. **📋 Inicialização:** 
   - Criação automática da estrutura A-SDLC
   - Geração do `PROJECT_CONTEXT.md` detalhado
   - Instalação dos 5 agentes especializados
   - Criação dos templates de prompts

2. **📝 Planejamento:**
   - Criação de stories com descrição de alto nível
   - Geração automática de planos detalhados pela LLM
   - Definição de manifestos de arquivos específicos
   - Estabelecimento de critérios de aceitação

3. **⚡ Implementação:**
   - Uso dos prompts profissionais com LLMs externas
   - Seguimento dos checklists dos agentes especializados
   - Implementação guiada por personas bem definidas
   - Validação contínua de conformidade

4. **✅ Validação:**
   - Verificação automática de implementação real
   - Validação de testes funcionais
   - Conformidade com padrões A-SDLC
   - Documentação atualizada

## 🎯 Tipos de Projeto Suportados

O A-SDLC adapta seus planos e agentes para diferentes tipos de projeto:

- **🌐 web_frontend** - Aplicações web frontend (HTML/CSS/JS, React, Vue)
- **🔌 web_api** - APIs web backend (Python FastAPI, Node.js Express)
- **🌐 web_fullstack** - Aplicações web completas (Frontend + Backend)
- **📱 mobile** - Aplicações móveis (React Native, Flutter)
- **💻 desktop** - Aplicações desktop (Electron, Tkinter)
- **🤖 cli** - Aplicações linha de comando

## 📁 Estrutura de Arquivos

```
A-SDLC-Framework/
├── asdlc/                    # 🧠 Core framework
│   ├── project_manager.py    # Gestão de projetos
│   ├── story_manager.py      # Gestão de stories
│   ├── plan_generator.py     # Geração de planos com LLM
│   ├── ui_manager.py         # Interface de usuário
│   └── llm_client.py         # Cliente para APIs de LLM
├── .asdlc/                   # 🤖 Configuração A-SDLC do framework
│   └── agents/               # Agentes especializados
├── prompts/                  # 📚 Templates para LLMs externas
├── examples/                 # 📖 Projetos de exemplo
├── tests/                    # 🧪 Testes do framework
├── main.py                   # 🚀 Ponto de entrada
├── PROJECT_CONTEXT.md        # 📋 Contexto do próprio framework
└── README.md                 # 📖 Esta documentação
```

## 🔧 Tecnologias

- **Python 3.8+** - Linguagem principal
- **OpenAI API** - Integração com GPT para geração de planos
- **argparse** - Interface de linha de comando
- **PyYAML** - Configurações e metadados
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📖 Documentação

Para mais detalhes sobre como usar o A-SDLC:

- **📋 [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Contexto técnico completo do framework
- **📚 [prompts/README.md](prompts/README.md)** - Como usar templates com LLMs externas
- **📖 [examples/](examples/)** - Projetos de exemplo implementados com A-SDLC
- **🇺🇸 [README_EN.md](README_EN.md)** - English version of this documentation

### 🔍 Exemplo de Comparação

Para demonstrar a diferença entre desenvolvimento tradicional e com A-SDLC:

- **📝 [examples/No A-SDLC/](examples/No%20A-SDLC/)** - TodoList implementada sem framework (para comparação)
- **📖 [examples/web_frontend/](examples/web_frontend/)** - TodoList implementada com A-SDLC

**Compare os dois exemplos** para ver como o A-SDLC melhora a qualidade, estrutura e profissionalismo do código.

## 🤝 Contribuição

Contribuições seguindo o processo A-SDLC são bem-vindas! 

1. Faça um fork do projeto
2. Crie uma story para sua melhoria usando o próprio A-SDLC
3. Implemente seguindo as personas dos agentes
4. Abra um Pull Request com documentação completa

## 📄 Licença

Este projeto está sob a licença MIT com restrições de uso não comercial.

### 📋 Termos de Uso

- **✅ Uso Livre:** Para projetos pessoais, educacionais e não comerciais
- **❌ Uso Comercial:** Proibido sem autorização explícita
- **📝 Atribuição:** Obrigatória em todos os usos
- **🔗 Citação:** Deve incluir referência ao framework A-SDLC

### 📝 Como Atribuir

Ao usar o A-SDLC Framework, inclua:

```markdown
Desenvolvido com [A-SDLC Framework](https://github.com/jota-f/asdlc-framework)
```

Ou em código:

```python
# Desenvolvido com A-SDLC Framework
# https://github.com/jota-f/asdlc-framework
```

### 🏢 Licenciamento Comercial

Para uso comercial, entre em contato para licenciamento específico.

---

**💡 Desenvolvido seguindo seus próprios padrões A-SDLC - Um framework que pratica o que ensina!**