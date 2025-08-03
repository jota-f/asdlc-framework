# 🆘 Guia de Suporte - A-SDLC Framework

## 📞 Como Obter Ajuda

### 🚀 Primeiros Passos

Antes de pedir ajuda, verifique:

1. **📖 Documentação:** Leia o [README](README.md) completo
2. **🔍 Issues:** Procure por problemas similares nas [issues](https://github.com/seu-usuario/asdlc-framework/issues)
3. **📚 Exemplos:** Consulte os [exemplos](examples/) fornecidos
4. **🔧 Configuração:** Verifique se o ambiente está configurado corretamente

### 📋 Checklist de Troubleshooting

- [ ] **Python 3.8+** instalado
- [ ] **Ambiente virtual** ativado
- [ ] **Dependências** instaladas (`pip install -r requirements.txt`)
- [ ] **API Key** configurada (`.env` file)
- [ ] **Permissões** de arquivo corretas
- [ ] **Conexão** com internet funcionando

## 🆘 Canais de Suporte

### 🐛 GitHub Issues

**Para bugs e problemas técnicos:**

1. **Procure** por issues similares
2. **Use o template** de bug report
3. **Inclua** logs e informações do ambiente
4. **Descreva** o problema detalhadamente

**Template rápido:**
```markdown
**Problema:** [Descrição]
**Ambiente:** [OS, Python, A-SDLC versão]
**Passos:** [Como reproduzir]
**Logs:** [Erros ou saídas]
```

### 💬 Discussões

**Para perguntas gerais e discussões:**

- **📚 Como usar:** Perguntas sobre funcionalidades
- **🤝 Melhores práticas:** Compartilhar experiências
- **💡 Ideias:** Sugestões e feedback
- **🎯 Casos de uso:** Exemplos práticos

## 🎯 Problemas Comuns

### ❌ "ModuleNotFoundError"

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### ❌ "OpenAI API Error"

**Solução:**
```bash
# Verificar arquivo .env
cat .env

# Configurar API key
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### ❌ "Permission Denied"

**Solução:**
```bash
# Verificar permissões
ls -la

# Corrigir permissões
chmod +x main.py
```

### ❌ "Project Creation Failed"

**Solução:**
```bash
# Verificar diretório atual
pwd

# Verificar espaço em disco
df -h

# Verificar permissões de escrita
touch test.txt && rm test.txt
```

## 📚 Recursos de Aprendizado

### 🎓 Tutoriais

- **🚀 [Primeiros Passos](examples/)** - Guia básico
- **📝 [Workflow Completo](README.md#workflow-a-sdlc)** - Processo completo
- **🤖 [Agentes Especializados](README.md#agentes-especializados)** - Como usar cada agente

### 📖 Documentação

- **📋 [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Contexto técnico
- **📚 [prompts/README.md](prompts/README.md)** - Como usar templates
- **📖 [CONTRIBUTING.md](CONTRIBUTING.md)** - Como contribuir

### 🎯 Exemplos Práticos

- **🌐 [Web Frontend](examples/web_frontend/)** - Aplicações web
- **🔌 [Web API](examples/web_api/)** - APIs backend
- **📱 [Mobile](examples/mobile/)** - Apps móveis
- **💻 [CLI](examples/cli/)** - Aplicações linha de comando

## 🔧 Ferramentas de Diagnóstico

### 📊 Verificação de Sistema

```bash
# Informações do sistema
python --version
pip list
python -c "import asdlc; print(asdlc.__version__)"
```

### 🧪 Teste de Conectividade

```bash
# Testar API OpenAI
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key configurada:', bool(os.getenv('OPENAI_API_KEY')))
"
```

### 📝 Logs Detalhados

```bash
# Executar com logs detalhados
python main.py --verbose --debug
```

## 🤝 Comunidade

### 👥 Contribuidores

- **👨‍💻 Desenvolvedores:** Código e funcionalidades
- **📚 Documentadores:** Guias e tutoriais
- **🧪 Testadores:** Bugs e melhorias
- **🎨 Designers:** Interface e UX

### 🌟 Reconhecimento

Contribuidores de suporte são reconhecidos:

- **📝 Mencionados** no README
- **🏆 Badges** de suporte
- **📢 Agradecimentos** em releases
- **💬 Acesso** a canais especiais

---

**💡 Todo contato e suporte deve ser feito exclusivamente via GitHub (issues, discussions, PRs).** 