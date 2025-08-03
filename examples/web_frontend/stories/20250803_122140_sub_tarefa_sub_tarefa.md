---
title: "sub tarefa"
ticket: "20250803_122140_sub_tarefa"
status: "CONCLUÍDO"
---

# Plano de Execução: sub tarefa

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: sub tarefa

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:** `src/components/SubTask.js`, `src/utils/storage.js`
- **MODIFICAR:** `src/script.js`, `src/index.html`

## 🎯 Tarefas Detalhadas

### Tarefa 1: Implementar componente de sub tarefa
1. **Arquivo a criar/modificar**: `src/components/SubTask.js`
2. **Referência de Contexto**: Componente para adicionar sub tarefas à lista de tarefas
3. **Ação**: Criar um novo componente React que permita a adição, remoção e marcação de sub tarefas.

#### 1.1 Componente SubTask
```javascript
// src/components/SubTask.js
import React, { useState } from 'react';

const SubTask = ({ onAdd, onRemove, subTask }) => {
    const [title, setTitle] = useState('');

    const handleAdd = () => {
        onAdd(title);
        setTitle('');
    };

    return (
        <div>
            <input 
                type="text" 
                value={title} 
                onChange={(e) => setTitle(e.target.value)} 
                placeholder="Adicionar Sub Tarefa" 
            />
            <button onClick={handleAdd}>Adicionar</button>
            <button onClick={() => onRemove(subTask.id)}>Remover</button>
        </div>
    );
};

export default SubTask;
```

### Tarefa 2: Modificar lógica de armazenamento
1. **Arquivo a criar/modificar**: `src/utils/storage.js`
2. **Ação**: Implementar funções para armazenar e recuperar sub tarefas do localStorage.

#### 2.1 Funções de Armazenamento
```javascript
// src/utils/storage.js
export const saveSubTasks = (tasks) => {
    localStorage.setItem('subTasks', JSON.stringify(tasks));
};

export const getSubTasks = () => {
    return JSON.parse(localStorage.getItem('subTasks')) || [];
};
```

### Tarefa 3: Integrar o novo componente no script principal
1. **Arquivo a criar/modificar**: `src/script.js`
2. **Ação**: Integrar o novo componente SubTask no fluxo do Todo App.

#### 3.1 Integração no script
```javascript
// src/script.js
import SubTask from './components/SubTask';
import { saveSubTasks, getSubTasks } from './utils/storage';

// Código de inicialização e manipulação de tarefas
const subTasks = getSubTasks();
const addSubTask = (title) => {
    subTasks.push({ title });
    saveSubTasks(subTasks);
};

// Renderizar SubTask
const renderSubTasks = () => {
    // lógica para renderizar sub tarefas
};

// Chamar renderSubTasks em cada alteração
```

## ✅ Critérios de Aceitação

- [ ] O componente SubTask deve ser capaz de adicionar e remover sub tarefas.
- [ ] As sub tarefas devem ser armazenadas e recuperadas corretamente do localStorage.
- [ ] A interface deve ser responsiva e acessível.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `subTask` para sub tarefas
  - `storage` para funções de armazenamento

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `task` - Use `subTask`
  - Nomes de variáveis não descritivos

### **Estrutura de Código**:
- Componentes React devem ser funcionais e reutilizáveis.
- Funções de armazenamento devem seguir a convenção de nomeação clara.

## 🎨 Princípios a Seguir

- **Segurança**: Validar entrada do usuário antes de armazenar.
- **Performance**: Minimizar acessos ao localStorage.
- **Logging**: Utilizar console.log para debugging durante o desenvolvimento.
- **Modularidade**: Separar lógica de componentes e utilitários.
- **Reutilização**: Criar componentes que possam ser utilizados em diferentes partes da aplicação.

## 📊 Métricas de Sucesso

### **Performance**:
- Tempo de resposta para adicionar/remover sub tarefas < 100ms.
- A aplicação deve carregar sub tarefas em menos de 200ms.

### **Estabilidade**:
- O localStorage deve ter 100% de precisão nas operações de leitura/escrita.
- Não deve haver erros na interface ao adicionar/remover sub tarefas.

### **Experiência do Usuário**:
- A interface deve ser intuitiva, com feedback visual ao adicionar/remover sub tarefas.
- Acessibilidade deve ser testada para garantir que todos os usuários possam interagir com a interface.

## ⏱️ Plano de Implementação

### **Fase 1: Desenvolvimento do Componente SubTask (2 horas)**
1. Criar o componente SubTask.
2. Implementar lógica de adição/removal de sub tarefas.
3. Testar o componente isoladamente.

### **Fase 2: Integração e Testes (1 hora)**
1. Integrar SubTask no fluxo principal do aplicativo.
2. Testar a persistência de dados no localStorage.
3. Garantir responsividade da interface.

**Tempo Total Estimado**: 3 horas
**Impacto**: Alto para a funcionalidade de gerenciamento de tarefas
**Risco**: Baixo (a funcionalidade é bem definida e modular)

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