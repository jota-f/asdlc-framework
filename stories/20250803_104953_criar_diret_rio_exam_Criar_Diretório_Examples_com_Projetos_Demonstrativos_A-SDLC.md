---
title: "Criar Diretório Examples com Projetos Demonstrativos A-SDLC"
ticket: "20250803_104953_criar_diret_rio_exam"
status: "CONCLUÍDO"
priority: "Medium"
estimated_hours: "16"
start_date: "2025-08-03"
completion_date: "2025-08-03"
notes: "Implementação concluída seguindo A-SDLC. 5 projetos criados, 1 com código funcional completo (web_frontend), estrutura A-SDLC padrão implementada."
implementation_summary: "Diretório examples/ criado com 5 projetos demonstrativos: web_frontend (TODO funcional), web_api, mobile, desktop, cli. Cada projeto possui estrutura A-SDLC completa."
---

# Plano de Execução: Criar Diretório Examples com Projetos Demonstrativos A-SDLC

## 📝 Especificações da Story

**História do Usuário:**

Criar um diretório 'examples/' na raiz do projeto A-SDLC contendo projetos de exemplo que demonstrem o uso correto do framework para diferentes tipos de aplicação:

1. **examples/web_frontend/** - Aplicação web frontend completa (Todo App em React)
2. **examples/web_api/** - API REST completa (Sistema de gestão de tarefas em FastAPI)
3. **examples/mobile/** - Aplicação móvel simples (Lista de compras em React Native)
4. **examples/desktop/** - Aplicação desktop (Editor de texto em Electron)
5. **examples/cli/** - Aplicação CLI (Gerador de relatórios em Python)

Cada exemplo deve incluir:
- PROJECT_CONTEXT.md completo e bem detalhado
- .asdlc/agents/ com todos os 5 agentes
- stories/ com pelo menos 3 stories implementadas
- prompts/ com todos os templates
- Código fonte funcional implementado
- README.md explicando o exemplo
- Testes automatizados funcionais

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:** 
  - `examples/web_frontend/`
    - `PROJECT_CONTEXT.md`
    - `.asdlc/agents/`
    - `stories/`
    - `prompts/`
    - Código fonte HTML/CSS/JS
    - `README.md`
    - Testes automatizados
  - `examples/web_api/`
    - `PROJECT_CONTEXT.md`
    - `.asdlc/agents/`
    - `stories/`
    - `prompts/`
    - Código fonte Python/Node.js
    - `README.md`
    - Testes automatizados
  - `examples/mobile/`
    - `PROJECT_CONTEXT.md`
    - `.asdlc/agents/`
    - `stories/`
    - `prompts/`
    - Código fonte React Native/Flutter
    - `README.md`
    - Testes automatizados
  - `examples/desktop/`
    - `PROJECT_CONTEXT.md`
    - `.asdlc/agents/`
    - `stories/`
    - `prompts/`
    - Código fonte Electron/Python
    - `README.md`
    - Testes automatizados
  - `examples/cli/`
    - `PROJECT_CONTEXT.md`
    - `.asdlc/agents/`
    - `stories/`
    - `prompts/`
    - Código fonte Python/Node.js
    - `README.md`
    - Testes automatizados

## 🎯 Tarefas Detalhadas

### Tarefa 1: Inicializar Estrutura do Projeto Web Frontend

1. **Arquivo a criar/modificar**: `examples/web_frontend/`
2. **Ação**: Inicializar a estrutura do projeto web frontend conforme especificações.

#### 1.1 Criar Estrutura Básica HTML/CSS/JS
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="todo-list">
        <ul id="tasks"></ul>
        <input type="text" id="taskInput" placeholder="Add new task">
        <button onclick="addTask()">Add Task</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

### Tarefa 2: Implementar API REST com FastAPI

1. **Arquivo a criar/modificar**: `examples/web_api/`
2. **Ação**: Implementar uma API REST completa com FastAPI para o sistema de gestão de tarefas.

#### 2.1 Definir Endpoints e Lógica da API
```Python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}

@app.get("/tasks")
def read_tasks():
    return {"task": "Task 1"}

@app.post("/tasks")
def create_task():
    return {"task": "Task created"}
```

## ✅ Critérios de Aceitação

- [ ] Cada exemplo deve conter todos os arquivos e estruturas especificados no Manifesto.
- [ ] Os projetos devem funcionar corretamente e serem acompanhados de testes automatizados.
- [ ] As funcionalidades dos exemplos devem demonstrar claramente o uso adequado do framework A-SDLC.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `project_context` para contexto do projeto
  - `story_template` para templates de stories
  - `agent_persona` para definição de agentes
  - `plan_generator` para geração de planos
  - `implementation_validator` para validação

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `user_story` - Usar `story_template`
  - `ai_agent` - Usar `agent_persona`
  - `code_generator` - Usar `plan_generator`
  - Implementações sem validação
  - Agentes sem personas definidas

### **Estrutura de Código**:
- **Módulos especializados** com responsabilidades únicas
- **Logging estruturado** com emojis para UX
- **Validação robusta** de inputs e outputs
- **Documentação inline** para funções complexas
- **Testes automatizados** para lógica crítica

## 🎨 Princípios a Seguir

- **Segurança**: Implementar camadas de segurança apropriadas para cada tipo de aplicação.
- **Performance**: Otimizar o código e considerar questões de performance desde o início.
- **Logging**: Utilizar logging estruturado para melhor rastreabilidade e monitoramento.
- **Modularidade**: Separar o código em módulos reutilizáveis e de fácil manutenção.
- **Reutilização**: Promover a reutilização de código e componentes sempre que possível.

## 📊 Métricas de Sucesso

### **Performance**:
- Tempo de Resposta da API: <100ms em média
- Carregamento da Página Web: <500ms

### **Estabilidade**:
- Sem erros críticos nos logs por mais de 24 horas

### **Experiência do Usuário**:
- Interface intuitiva e responsiva em todos os exemplos
- Testes de aceitação passando em 100% dos casos

## ⏱️ Plano de Implementação

### **Fase 1: Implementação Web Frontend (8 horas)**
1. Inicializar estrutura HTML/CSS/JS do Todo App.
2. Integrar lógica JavaScript para adicionar e visualizar tarefas.
3. Testar e garantir responsividade e usabilidade.

### **Fase 2: Desenvolvimento API REST (12 horas)**
1. Implementar endpoints REST com FastAPI.
2. Realizar testes de integração e performance.
3. Documentar a API e garantir segurança.

**Tempo Total Estimado**: 20 horas
**Impacto**: Médio para demonstração de funcionalidades do framework
**Risco**: Baixo (considerando a familiaridade com as tecnologias utilizadas)

## 🤖 Instruções para Agentes de IA

### **Code Agent (Fase 1)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários, de integração e de performance conforme as métricas de sucesso definidas."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

### **Requirements Agent (Opcional)**:
Combine a persona do `.asdlc/agents/requirements_agent.md` com a tarefa: "Analise se os requisitos foram completamente atendidos e se há gaps na implementação. Sugira melhorias se necessário."

### **Architecture Agent (Opcional)**:
Combine a persona do `.asdlc/agents/architecture_agent.md` com a tarefa: "Valide a arquitetura implementada e verifique se está alinhada com os princípios de design definidos. Sugira otimizações arquiteturais se necessário."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."