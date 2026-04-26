---
title: "RCA_Fix_Final_V2"
ticket: "20260426_010556_rca_fix_final_v2"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: RCA_Fix_Final_V2

## 📝 Especificações da Story

**História do Usuário:**  
Como mantenedor do framework A-SDLC, quero corrigir a falha remanescente no ciclo de feedback de autocorreção, garantindo que o agente executor reavalie e corrija automaticamente erros detectados pelo `validation_checker` sem interrupções ou loops infinitos.

**Contexto:**  
A versão anterior (RCA_Fix_Final) introduziu melhorias no Harness Feedback Loop, mas ainda ocorrem situações em que o `agent_executor` ignora o resultado da validação ou entra em retry excessivo. Este fix V2 resolve a raiz do problema: a integração entre `agent_executor`, `validation_checker` e o gerenciamento de tentativas.

## Manifesto de Arquivos (Gerado por IA)

- **MODIFICAR:**
  - `asdlc/agent_executor.py` — aprimorar lógica de retry com limite configurável e análise de causa raiz
  - `asdlc/validation_checker.py` — adicionar tipagem de erros (bloqueante vs. advertência) e relatório de diagnóstico
  - `asdlc/utils.py` — incluir helper `classify_error()` para classificação de falhas
  - `main.py` — expor parâmetro `--max-retries` na CLI

- **CRIAR:**
  - `tests/test_rca_fix_v2.py` — testes unitários e de integração para o novo comportamento

## 🎯 Tarefas Detalhadas

### Tarefa 1: Refatorar o Validation Checker para emitir diagnóstico estruturado
1. **Arquivo a modificar**: `asdlc/validation_checker.py`
2. **Referência de Contexto**: `PROJECT_CONTEXT.md` → Harness Engineering & Feedback Loops
3. **Ação**: Modificar `validate()` para retornar um dicionário com chave `status` ("pass", "warning", "fail") e `diagnosis` com detalhes.

#### 1.1 Novo formato de resposta
```python
def validate(self, code: str, context: dict) -> dict:
    issues = self._lint(code)
    if not issues:
        return {"status": "pass", "diagnosis": "No issues found."}
    critical = any("E" in issue for issue in issues)
    return {
        "status": "fail" if critical else "warning",
        "diagnosis": "; ".join(issues)
    }
```

### Tarefa 2: Adicionar classificador de erro no módulo de utilitários
1. **Arquivo a modificar**: `asdlc/utils.py`
2. **Ação**: Criar função `classify_error()`.

#### 2.1 Function helper
```python
def classify_error(validation_result: dict) -> str:
    if validation_result["status"] == "pass":
        return "success"
    if "indentation" in validation_result["diagnosis"].lower():
        return "style"
    if "undefined" in validation_result["diagnosis"].lower():
        return "logic"
    return "unknown"
```

### Tarefa 3: Aprimorar Agent Executor com lógica de retry inteligente
1. **Arquivo a modificar**: `asdlc/agent_executor.py`
2. **Ação**: Alterar `execute_with_feedback()` para interpretar o diagnóstico, limitar tentativas por tipo de erro, e registrar a causa raiz.

#### 3.1 Loop de feedback aprimorado
```python
async def execute_with_feedback(self, task: str, max_retries: int = 3):
    for attempt in range(max_retries):
        code = await self._run_agent(task)
        validation = self.validator.validate(code, self.context)
        if validation["status"] == "pass":
            return code
        error_type = classify_error(validation)
        if error_type == "style":
            self._auto_fix_style(code)
            continue
        if attempt == max_retries - 1:
            raise ExecutionError(f"RCA: {validation['diagnosis']}")
        task = self._refine_task(task, validation["diagnosis"])
```

### Tarefa 4: Expor `max_retries` na CLI
1. **Arquivo a modificar**: `main.py`
2. **Ação**: Adicionar argumento opcional `--max-retries` com valor padrão 3.

#### 4.1 Alteração no parser
```python
parser.add_argument('--max-retries', type=int, default=3, help='Número máximo de tentativas de autocorreção')
```

### Tarefa 5: Criar suíte de testes
1. **Arquivo a criar**: `tests/test_rca_fix_v2.py`

#### 5.1 Teste de retry com erro de lógica
```python
def test_retry_on_logic_error():
    validator = ValidationChecker()
    validator._lint = Mock(return_value=["E: undefined variable"])
    executor = AgentExecutor(validator=validator)
    with pytest.raises(ExecutionError):
        asyncio.run(executor.execute_with_feedback("print(x)", max_retries=2))
```

## ✅ Critérios de Aceitação

- [ ] `validation_checker` sempre retorna um dict com `status` e `diagnosis`  
- [ ] Erros de estilo são corrigidos automaticamente sem consumir tentativa  
- [ ] Erros de lógica disparam re‑refinamento da task até `max_retries`  
- [ ] Após esgotar tentativas, uma `ExecutionError` é levantada com a causa raiz  
- [ ] CLI aceita `--max-retries` e repassa ao executor  
- [ ] Nenhum loop infinito ocorre em cenário de erro persistente  

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `status` (pass | warning | fail)
  - `diagnosis` (string descritiva)
  - `RCA` (Root Cause Analysis)
  - `agent`, `harness`, `feedback loop`

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `error_code` (substituído por `classify_error`)
  - `while True` no loop de feedback (usar `for attempt in range`)

### **Estrutura de Código**:
- Funções assíncronas no executor devem seguir o padrão `async def`
- Todas as classes de exceção herdam de `ASDLCException`

## 🎨 Princípios a Seguir

- **Segurança**: Não expor stack traces nos diagnósticos enviados ao usuário  
- **Performance**: Validação não deve adicionar mais de 50 ms ao ciclo  
- **Logging**: Usar `logging.getLogger(__name__)` com níveis adequados  
- **Modularidade**: `classify_error()` deve residir em `utils`, não no executor  
- **Reutilização**: `ValidationChecker` permanece agnóstico ao tipo de agente  

## 📊 Métricas de Sucesso

### **Performance**:
- Tempo médio de validação < 50 ms
- Retry máximo de 3 tentativas em erros de lógica

### **Estabilidade**:
- Zero ocorrências de loop infinito nos testes de stress
- 100% das falhas capturadas pela `ExecutionError` com diagnóstico

### **Experiência do Usuário**:
- Mensagens de erro no CLI exibem a causa raiz de forma legível
- Comportamento padrão (sem `--max-retries`) permanece funcional

## ⏱️ Plano de Implementação

### **Fase 1: Core Fix (1h)**
1. Editar `validation_checker.py`
2. Criar `classify_error` em `utils.py`
3. Atualizar `agent_executor.py`

### **Fase 2: CLI e Testes (45min)**
1. Adicionar argumento `--max-retries` em `main.py`
2. Escrever `test_rca_fix_v2.py`
3. Executar suite de regressão (`pytest`)

**Tempo Total Estimado**: 1h45min  
**Impacto**: Alto para a confiabilidade do ciclo de autocorreção  
**Risco**: Baixo (mudanças isoladas, sem quebra de API pública)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide se a RCA descrita faz sentido técnico e se o teste de reprodução cobre o cenário relatado."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários, de integração e de performance conforme as métricas de sucesso definidas."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."