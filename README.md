# 🌌 A-SDLC Framework (v2.2.0)
**AI-Driven Software Development Lifecycle**

O A-SDLC é um framework de engenharia de software desenhado para transformar IAs em agentes autônomos capazes de gerenciar o ciclo de vida completo de um projeto. Ele utiliza **Harness Engineering**, **Recursive Handoffs** e **Feedback Loops** para garantir código de alta fidelidade.

---

## 📍 Sumário
- [🚀 O que é o A-SDLC?](#-o-que-é-o-a-sdlc)
- [⚙️ Instalação e Setup](#️-instalação-e-setup)
- [🧠 Modo MCP (Antigravity Power)](#-modo-mcp-antigravity-power)
- [🛠️ Modo Agentic (IDE Templates)](#️-modo-agentic-ide-templates)
- [🏃 Como Começar (Workflow)](#-como-começar-workflow)
- [📂 Estrutura de Trabalho Recomendada](#-estrutura-de-trabalho-recomendada)
- [📖 Exemplos e Casos de Uso](#-exemplos-e-casos-de-uso)
- [📄 Termos de Uso](#-termos-de-uso)

---

## 🚀 O que é o A-SDLC?
Diferente de simples assistentes de chat, o A-SDLC trata a IA como um **Sistema Multi-Agente (MAS)**. Cada tarefa é passada por especialistas (Requisitos, Arquitetura, Código, Testes) que validam o trabalho uns dos outros através de um "Harness" (arreio) que monitora erros em tempo real.

---

## ⚙️ Instalação e Setup

### 1. Requisitos
- Python 3.10+
- Git

### 2. Clonagem e Dependências
```bash
git clone https://github.com/jota-f/A-SDLC.git
cd A-SDLC
pip install -r requirements.txt
cp .env.example .env
```

---

## 🧠 Modo MCP (Antigravity Power)
Este é o modo mais avançado. Ele conecta o framework diretamente à sua IDE (Cursor/Windsurf) via **Model Context Protocol**, permitindo que o framework use a inteligência da IDE sem precisar de chaves de API externas.

### Como instalar o servidor MCP:
1. **Instale as bibliotecas**: `pip install fastmcp mcp`
2. **Configure sua IDE**: Adicione o servidor ao seu arquivo `mcp_config.json`:
```json
"asdlc": {
  "command": "python",
  "args": ["C:/Caminho/Para/A-SDLC/asdlc/mcp_server.py"],
  "env": { "PYTHONPATH": "C:/Caminho/Para/A-SDLC" }
}
```
3. **Reinicie a IDE**. Agora eu (Antigravity) terei "ferramentas" nativas do A-SDLC para criar projetos e stories para você!

---

## 🛠️ Modo Agentic (IDE Templates)
Se você não quer usar a Engine Python e prefere trabalhar apenas no chat da IDE:
1. Copie a pasta `agentic_templates/` para o seu projeto.
2. Use `@asdlc-plan.md` para planejar e `@asdlc-coder.md` para codificar.
3. [Veja o Guia Detalhado aqui](agentic_templates/README.md).

---

## 🏃 Como Começar (Workflow)

### Cenário A: Projeto Novo
```bash
python main.py create-project --name "meu_app" --prompt "Descrição do app"
```

### Cenário B: Projeto Existente (Integração)
```bash
python main.py create-project --name "meu_projeto" --path "C:/pasta/do/projeto" --prompt "Análise"
```

---

## 📂 Estrutura de Trabalho Recomendada
Para evitar confusão entre os arquivos do framework e seus códigos, recomendamos:
```text
C:/Dev/
  ├── A-SDLC/             <-- O Framework (central)
  ├── Projeto_Alpha/      <-- Seu projeto (com .asdlc e stories instalados)
  └── Projeto_Beta/       <-- Outro projeto seu
```

---

## 📖 Exemplos e Casos de Uso

### 🚗 Sensor de Fadiga (Arduino/ESP32)
Um exemplo real de como o A-SDLC pode ser usado em sistemas embarcados.
- **Local**: `test_projects/drowsinessSensor`
- **Destaque**: Uso de sensores de feedback para validar compilação de firmware.

### 📝 TodoList Fullstack
Exemplo clássico para entender o fluxo de requisitos até o teste E2E.
- **Local**: `examples/web_fullstack`

---

## 📄 Termos de Uso
Este framework é sob licença MIT, mas com restrição: **Uso comercial proibido sem autorização**.
- **Livre**: Uso pessoal, acadêmico e open-source.
- **Atribuição**: Obrigatório citar "Desenvolvido com A-SDLC Framework".

---
**💡 A-SDLC: Onde o código não é apenas escrito, ele é projetado por máquinas e validado por regras.**