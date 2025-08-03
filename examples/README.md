# 📖 Exemplos A-SDLC Framework

Este diretório contém **5 projetos de exemplo** que demonstram o uso prático do framework **A-SDLC (AI-Driven Software Development Lifecycle)** para diferentes tipos de aplicações.

## 🎯 Objetivo dos Exemplos

Cada projeto neste diretório serve como uma **implementação de referência** do A-SDLC, mostrando:

- ✅ **Estrutura Padrão**: Como organizar projetos seguindo A-SDLC
- ✅ **Agentes Especializados**: Uso das 5 personas em projetos reais
- ✅ **Stories Estruturadas**: Planejamento detalhado de funcionalidades
- ✅ **Código Funcional**: Implementações práticas e funcionais
- ✅ **Documentação Completa**: Padrões de documentação A-SDLC
- ✅ **Boas Práticas**: Exemplos de qualidade profissional

## 📂 Projetos Disponíveis

### 🌐 1. Web Frontend - Todo App
**Diretório**: `web_frontend/`  
**Tecnologia**: HTML5 + CSS3 + JavaScript Vanilla  
**Descrição**: Aplicação de gerenciamento de tarefas com interface moderna e responsiva.

**Funcionalidades**:
- Adicionar/remover/marcar tarefas
- Filtros (todas, pendentes, concluídas)
- Persistência local (localStorage)
- Design responsivo e acessível
- Notificações toast

**Status**: ✅ **IMPLEMENTADO** - Código funcional completo

---

### 🔌 2. Web API - Task Manager API
**Diretório**: `web_api/`  
**Tecnologia**: FastAPI (Python)  
**Descrição**: API REST para sistema de gestão de tarefas com autenticação JWT.

**Funcionalidades**:
- CRUD completo de tarefas
- Autenticação JWT
- Validação de dados (Pydantic)
- Documentação automática (Swagger)
- Integração com SQLite

**Status**: 🔄 **ESTRUTURA CRIADA** - Implementação pendente

---

### 📱 3. Mobile - Shopping List App
**Diretório**: `mobile/`  
**Tecnologia**: React Native  
**Descrição**: Aplicativo móvel para lista de compras com sincronização offline.

**Funcionalidades**:
- Adicionar/remover itens
- Categorização de produtos
- Modo offline
- Interface otimizada para touch
- Dark mode

**Status**: 🔄 **ESTRUTURA CRIADA** - Implementação pendente

---

### 💻 4. Desktop - Text Editor
**Diretório**: `desktop/`  
**Tecnologia**: Electron  
**Descrição**: Editor de texto desktop com syntax highlighting básico.

**Funcionalidades**:
- Criar/abrir/salvar arquivos
- Syntax highlighting
- Busca/substituir texto
- Múltiplas abas
- Configurações de tema

**Status**: 🔄 **ESTRUTURA CRIADA** - Implementação pendente

---

### 🤖 5. CLI - Report Generator
**Diretório**: `cli/`  
**Tecnologia**: Python  
**Descrição**: Ferramenta CLI para gerar relatórios de dados.

**Funcionalidades**:
- Ler arquivos CSV/JSON
- Filtrar e processar dados
- Gerar relatórios (TXT, CSV, PDF)
- Visualizações básicas
- Configuração via argumentos

**Status**: 🔄 **ESTRUTURA CRIADA** - Implementação pendente

## 🏗️ Estrutura Padrão A-SDLC

Cada projeto segue a mesma estrutura padrão do A-SDLC:

```
projeto-exemplo/
├── PROJECT_CONTEXT.md      # Contexto técnico completo
├── README.md               # Documentação específica
├── .asdlc/                 # Configuração A-SDLC
│   └── agents/             # 5 agentes especializados
│       ├── code_agent.md
│       ├── test_agent.md
│       ├── architecture_agent.md
│       ├── requirements_agent.md
│       └── review_agent.md
├── stories/                # Planejamento de funcionalidades
│   └── *.md               # Stories estruturadas
├── prompts/                # Templates para LLMs
│   ├── project_description_generator.md
│   ├── story_generator.md
│   ├── implementation_executor.md
│   ├── validation_checker.md
│   └── README.md
└── src/                    # Código fonte (estrutura varia)
```

## 🚀 Como Usar os Exemplos

### 1. **Explorar a Estrutura**
```bash
cd examples/web_frontend
ls -la                      # Ver estrutura completa
```

### 2. **Executar o Projeto**
```bash
# Para web_frontend (exemplo funcional)
cd examples/web_frontend
python -m http.server 8000  # Ou abrir index.html no navegador
```

### 3. **Estudar os Agentes**
```bash
cat .asdlc/agents/code_agent.md      # Examinar persona do Code Agent
cat .asdlc/agents/test_agent.md      # Examinar persona do Test Agent
```

### 4. **Analisar Stories**
```bash
ls stories/                          # Ver stories criadas
cat stories/20250803_*.md           # Examinar plano de implementação
```

### 5. **Validar Conformidade**
```bash
cd examples/web_frontend
python ../../main.py validate       # Verificar conformidade A-SDLC
```

## 🎓 Aprendizado com os Exemplos

### **Para Iniciantes**:
1. **Comece com `web_frontend`** - Implementação completa e funcional
2. **Estude o `PROJECT_CONTEXT.md`** - Entenda a estrutura de documentação
3. **Analise as stories** - Veja como funcionalidades são planejadas
4. **Examine os agentes** - Compreenda as diferentes personas

### **Para Desenvolvedores Experientes**:
1. **Compare implementações** - Veja diferenças entre tipos de projeto
2. **Estude os prompts** - Entenda como usar LLMs externas
3. **Valide conformidade** - Use o validador automático
4. **Contribua** - Implemente os exemplos restantes

### **Para Arquitetos**:
1. **Analise as decisões** - Entenda escolhas arquiteturais
2. **Compare padrões** - Veja adaptação A-SDLC por tipo de projeto
3. **Estude métricas** - Veja definição de critérios de qualidade

## 🤝 Contribuindo com Novos Exemplos

Para adicionar novos exemplos seguindo A-SDLC:

### 1. **Criar Projeto**
```bash
cd examples
python ../main.py create-project --name "novo-exemplo" --prompt "Descrição detalhada" --type "tipo"
```

### 2. **Implementar Código**
- Siga o plano gerado na story inicial
- Use as personas dos agentes como guia
- Implemente código funcional e testes

### 3. **Documentar**
- Crie README específico do projeto
- Documente decisões técnicas
- Inclua instruções de execução

### 4. **Validar**
```bash
python ../main.py validate --project .
```

### 5. **Atualizar Este README**
- Adicione o novo exemplo na lista
- Atualize estatísticas e contadores

## 📊 Status de Implementação

| Projeto | Estrutura | Código | Testes | Docs | Status |
|---------|-----------|--------|--------|------|--------|
| **web_frontend** | ✅ | ✅ | ⚠️ | ✅ | **COMPLETO** |
| **web_api** | ✅ | ❌ | ❌ | ✅ | Estrutura |
| **mobile** | ✅ | ❌ | ❌ | ✅ | Estrutura |
| **desktop** | ✅ | ❌ | ❌ | ✅ | Estrutura |
| **cli** | ✅ | ❌ | ❌ | ✅ | Estrutura |

**Progresso Geral**: 1/5 exemplos com implementação completa (20%)

## 🎯 Próximos Passos

### **Implementações Prioritárias**:
1. **web_api** - API REST com FastAPI (mais demandado)
2. **cli** - Ferramenta Python (mais simples de implementar)
3. **mobile** - React Native (conhecimento específico)
4. **desktop** - Electron (mais complexo)

### **Melhorias Gerais**:
- [ ] Testes automatizados para todos os exemplos
- [ ] CI/CD pipeline para validação contínua
- [ ] Docker containers para execução isolada
- [ ] Documentação em vídeo/tutorial
- [ ] Métricas de performance implementadas

## 🔗 Links Úteis

- **📚 Framework A-SDLC**: `../README.md`
- **🔍 Validador**: `python ../main.py validate`
- **📋 Paper Original**: `../Método Otimizado para Agentes Codificadores_.pdf`
- **🤖 Agentes**: Estude os arquivos `.asdlc/agents/` em qualquer exemplo

---

**🚀 Estes exemplos demonstram o poder do A-SDLC Framework na prática!**

*Use-os como referência, estude as implementações e contribua com melhorias seguindo sempre os padrões A-SDLC.*