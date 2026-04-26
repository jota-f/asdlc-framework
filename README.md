# 🌌 A-SDLC Framework (v2.3.0)
**AI-Driven Software Development Lifecycle**

O A-SDLC é um framework de engenharia de software desenhado para transformar IAs em agentes autônomos capazes de gerenciar o ciclo de vida completo de um projeto. Ele utiliza **Harness Engineering**, **Recursive Handoffs** e **Feedback Loops** para garantir código de alta fidelidade.

---

## 📍 Sumário
- [🚀 O que é o A-SDLC?](#-o-que-é-o-a-sdlc)
- [⚙️ Instalação e Setup](#️-instalação-e-setup)
- [🔀 Escolhendo o Motor de Execução](#-escolhendo-o-motor-de-execução)
- [🧠 Modo Antigravity (Padrão)](#-modo-antigravity-padrão)
- [⚡ Modo API Externa](#-modo-api-externa)
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

### 3. Configurar o MCP (IDE Integration)
```bash
pip install fastmcp mcp
```
Adicione ao `mcp_config.json` da sua IDE:
```json
"asdlc": {
  "command": "python",
  "args": ["C:/Caminho/Para/A-SDLC/asdlc/mcp_server.py"],
  "env": { "PYTHONPATH": "C:/Caminho/Para/A-SDLC" }
}
```
Reinicie a IDE após configurar.

---

## 🔀 Escolhendo o Motor de Execução

O A-SDLC tem **dois motores** que podem ser trocados a qualquer momento via `.env`:

| | 🧠 Modo Antigravity (Padrão) | ⚡ Modo API Externa |
|---|---|---|
| **Quem pensa?** | A IDE (Antigravity/Cursor) | API OpenAI |
| **Custo** | Zero (usa o modelo da IDE) | Pago (tokens da OpenAI) |
| **Configuração** | `ASDLC_ENGINE=antigravity` | `ASDLC_ENGINE=external` |
| **Como funciona** | Você pede no chat, a IDE codifica e testa | Script Python roda sozinho no terminal |
| **Ideal para** | Projetos grandes, economia, controle | Automação 100% sem intervenção |

### Como trocar:
Edite o arquivo `.env` na raiz do A-SDLC:
```env
# Para usar o Antigravity (padrão, sem custo):
ASDLC_ENGINE=antigravity

# Para usar a API OpenAI (requer OPENAI_API_KEY):
ASDLC_ENGINE=external
```

---

## 🧠 Modo Antigravity (Padrão)
Neste modo, a IDE é o "cérebro". O MCP serve como **ferramenta de gestão** (criar stories, atualizar status, métricas).

### Ferramentas MCP disponíveis:
| Ferramenta | Função |
|---|---|
| `asdlc_create_project` | Inicializa um projeto A-SDLC |
| `asdlc_create_story` | Cria uma nova story |
| `asdlc_get_story_details` | Lê o conteúdo de uma story |
| `asdlc_update_story_status` | Atualiza status (Todo/Done/Failed) |
| `asdlc_list_stories` | Lista todas as stories |
| `asdlc_get_project_metrics` | Métricas de progresso |
| `asdlc_validate_project` | Valida conformidade A-SDLC |

### Como implementar uma story:
No chat da IDE, diga:
> *"Use a Skill @asdlc_implementation para implementar a story @stories/ID_DA_STORY.md"*

A IDE vai: ler a story → codificar → rodar testes → corrigir erros → marcar DONE.

---

## ⚡ Modo API Externa
Neste modo, o script Python assume o controle total. Ele usa a API OpenAI para spawnar agentes autônomos.

### Ferramentas MCP adicionais:
| Ferramenta | Função |
|---|---|
| `asdlc_implement_story` | Execução autônoma via agentes Python |
| `asdlc_spawn_specialist` | Invoca um agente ad-hoc |

### Como implementar uma story:
```bash
python main.py implement --id 20260425_204837
```

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