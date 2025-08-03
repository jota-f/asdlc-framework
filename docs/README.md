# 📚 Documentação - A-SDLC Framework

Este diretório contém a documentação completa do A-SDLC Framework.

## 📁 Estrutura

```
docs/
├── README.md              # Este arquivo
├── source/                # Código fonte da documentação
│   ├── conf.py           # Configuração do Sphinx
│   ├── index.rst         # Página inicial
│   ├── api/              # Documentação da API
│   ├── guides/           # Guias de uso
│   └── examples/         # Exemplos práticos
├── build/                # Documentação gerada
│   └── html/             # Versão HTML
└── Makefile              # Comandos para gerar docs
```

## 🚀 Como Gerar a Documentação

### Pré-requisitos

```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

### Comandos

```bash
# Gerar documentação HTML
make html

# Gerar documentação PDF
make latexpdf

# Limpar arquivos gerados
make clean

# Servir documentação localmente
python -m http.server 8000 -d build/html
```

## 📖 Conteúdo da Documentação

### 🎯 Guias de Uso
- **Instalação e Configuração**
- **Primeiros Passos**
- **Workflow Completo**
- **Melhores Práticas**

### 🔧 Referência da API
- **ProjectManager** - Gestão de projetos
- **StoryManager** - Gestão de stories
- **PlanGenerator** - Geração de planos
- **UIManager** - Interface de usuário
- **LLMClient** - Cliente para LLMs

### 📝 Exemplos Práticos
- **Projetos Web Frontend**
- **APIs Backend**
- **Aplicações Mobile**
- **CLIs**
- **Aplicações Desktop**

### 🤖 Agentes Especializados
- **Code Agent** - Desenvolvedor Sênior
- **Test Agent** - QA Engineer
- **Architecture Agent** - Arquiteto
- **Requirements Agent** - Analista
- **Review Agent** - Code Reviewer

## 🎨 Tema

A documentação usa o tema **Read the Docs** para uma aparência profissional e responsiva.

## 🔄 Atualização Automática

A documentação é atualizada automaticamente via GitHub Actions quando há mudanças no código.

---

**💡 Dica:** Use `make html` para gerar a documentação localmente e visualizar as mudanças antes de fazer commit. 