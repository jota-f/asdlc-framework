---
title: "Teste de Modelo V4"
ticket: "20260425_224852_teste_de_modelo_v4"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: Teste de Modelo V4

## 📝 Especificações da Story

**História do Usuário:**  
Como desenvolvedor do framework A-SDLC, desejo um módulo de testagem específico para o Modelo V4 a fim de validar automaticamente sua saída, medir performance e detectar regressões, garantindo que as LLMs gerem planos de execução consistentes e aderentes aos padrões do framework.

**Descrição Técnica:**  
Implementar uma suíte de testagem (`ModelV4Tester`) que opere no contexto do Harness Engineering do A-SDLC, utilizando feed forward (injeção de contexto) e feedback loop (validação automática) para assegurar a qualidade do modelo. O módulo deve ser integrado ao fluxo do Plan Generator e ser capaz de delegar subtarefas (Recursive Handoff) para agentes especializados quando anomalias forem detectadas.

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:**
  - `asdlc/testing/__init__.py`
  - `asdlc/testing/model_v4_tester.py`
  - `tests/unit/test_model_v4.py`
  - `pytest.ini`
- **MODIFICAR:**
  - `asdlc/core/planner.py` (adicionar integração com o módulo de testagem)
  - `asdlc/harness/orchestrator.py` (opcional, para adicionar sensor de validação do modelo)

## 🎯 Tarefas Detalhadas

### Tarefa 1: Estruturar o módulo de testagem do Modelo V4
1. **Arquivo a criar/modificar**: `asdlc/testing/__init__.py`
2. **Referência de Contexto**: Estrutura modular do framework (conforme `PROJECT_CONTEXT.md`)
3. **Ação**: Criar o pacote `testing` e garantir que seja importável como `asdlc.testing`.

#### 1.1 Inicialização do pacote
```python
# asdlc/testing/__init__.py
"""Módulo de testagem de modelos do A-SDLC."""

from .model_v4_tester import ModelV4Tester

__all__ = ["ModelV4Tester"]
```

2. **Arquivo a criar**: `asdlc/testing/model_v4_tester.py`
3. **Ação**: Implementar a classe `ModelV4Tester` com métodos para:
   - Validação de sintaxe da resposta do modelo.
   - Verificação de consistência semântica (via heurísticas e chamadas a agentes de review).
   - Medição de latência e tokens.
   - Integração com o harness para disparar retentativas automáticas (Self-Healing).
   - Capacidade de handoff recursivo para o `bug_hunter_agent` em caso de falha.

#### 1.2 Esqueleto da classe
```python
# asdlc/testing/model_v4_tester.py
import time
import logging
from typing import Dict, Any

class ModelV4Tester:
    """Harness de teste específico para o Modelo V4."""
    
    def __init__(self, agent_executor, config=None):
        self.executor = agent_executor
        self.logger = logging.getLogger(__name__)
        # Configuração padrão
        self.config = {
            "max_retries": 3,
            "syntax_threshold": 0.95,
            "semantic_threshold": 0.90,
            "timeout_seconds": 10.0
        }
        if config:
            self.config.update(config)
    
    def run_syntax_validation(self, raw_output: str) -> bool:
        """Verifica se a saída é um YAML/Markdown válido conforme especificação."""
        pass  # Implementação conforme necessidade
    
    def run_semantic_validation(self, plan: Dict[str, Any]) -> bool:
        """Valida a coerência do plano gerado (presença de tarefas, arquivos, etc.)."""
        required_keys = ["tarefas", "manifesto", "criterios"]
        return all(k in plan for k in required_keys)
    
    def measure_performance(self, start_time: float, tokens_used: int) -> Dict[str, float]:
        """Retorna métricas de latência e eficiência."""
        return {
            "latency_seconds": time.time() - start_time,
            "tokens_per_second": tokens_used / (time.time() - start_time) if start_time else 0
        }
    
    def execute_with_feedback_loop(self, generator_fn, *args, **kwargs) -> Any:
        """Executa o modelo com retentativas automáticas e handoff."""
        for attempt in range(self.config["max_retries"]):
            start = time.time()
            raw_output, metadata = generator_fn(*args, **kwargs)
            perf = self.measure_performance(start, metadata.get("tokens", 0))
            syntax_ok = self.run_syntax_validation(raw_output)
            if not syntax_ok:
                self.logger.warning("Falha na validação de sintaxe – tentativa %d", attempt+1)
                continue
            plan = self.parse_plan(raw_output)
            if not self.run_semantic_validation(plan):
                self.logger.warning("Plano semanticamente inválido – handoff para Bug Hunter")
                # Recursive Handoff: delegar para agente especializado
                self.executor.delegate("bug_hunter", context=raw_output)
                continue
            return plan, perf
        raise RuntimeError("Testagem do Modelo V4 falhou após todas as tentativas.")
```

### Tarefa 2: Integrar com o Plan Generator
1. **Arquivo a modificar**: `asdlc/core/planner.py`
2. **Ação**: No método que chama a LLM para gerar o plano, instanciar `ModelV4Tester` e usar seu método `execute_with_feedback_loop` para validar a saída antes de retornar ao usuário.

#### 2.1 Exemplo de integração
```python
# asdlc/core/planner.py
from asdlc.testing import ModelV4Tester

class PlanGenerator:
    def __init__(self, agent_executor):
        self.tester = ModelV4Tester(agent_executor)
    
    def generate_plan(self, story):
        try:
            plan, metrics = self.tester.execute_with_feedback_loop(
                self._call_model_v4, story=story
            )
            return plan
        except RuntimeError as e:
            raise PlanGenerationError("Falha na geração do plano após validação rigorosa") from e
```

### Tarefa 3: Criar testes unitários
1. **Arquivo a criar**: `tests/unit/test_model_v4.py`
2. **Ação**: Escrever testes utilizando `pytest` para todos os métodos do `ModelV4Tester`, incluindo cenários de falha e o fluxo completo de feedback.

#### 3.1 Exemplos de teste
```python
# tests/unit/test_model_v4.py
import pytest
from asdlc.testing.model_v4_tester import ModelV4Tester

def test_syntax_validation_valid_output():
    tester = ModelV4Tester(agent_executor=None)
    valid_yaml = """
    tarefas:
      - nome: "T1"
    manifesto:
      - criar: "a.py"
    criterios:
      - "Tudo ok"
    """
    assert tester.run_syntax_validation(valid_yaml) == True

def test_feedback_loop_raises_after_retries(monkeypatch):
    # Simula função geradora sempre falhando
    def failing_gen(*args, **kwargs):
        return "inválido", {}
    monkeypatch.setattr(tester, '_call_model_v4', failing_gen)
    tester = ModelV4Tester(agent_executor=MockExecutor())
    with pytest.raises(RuntimeError):
        tester.execute_with_feedback_loop(tester._call_model_v4, story="test")
```

### Tarefa 4: Configurar pytest.ini para cobertura
1. **Arquivo a criar**: `pytest.ini`
2. **Ação**: Definir configurações básicas de teste.

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --strict-markers -v --cov=asdlc/testing --cov-report=term-missing
```

## ✅ Critérios de Aceitação

- [ ] O módulo `asdlc.testing` é importável e a classe `ModelV4Tester` está funcional.
- [ ] A validação de sintaxe rejeita saídas não conformes com o formato esperado (YAML inválido, markdown malformado).
- [ ] A validação semântica garante que planos gerados contenham os campos obrigatórios (`tarefas`, `manifesto`, `criterios`).
- [ ] O loop de feedback realiza até 3 tentativas e aciona o `bug_hunter_agent` via handoff quando a saída é semanticamente inválida.
- [ ] O `PlanGenerator` utiliza o `ModelV4Tester` e falha controladamente (lança exceção) após todas as tentativas.
- [ ] Os testes unitários cobrem >80% das linhas do módulo `model_v4_tester.py`.
- [ ] O teste de integração simula uma geração real e valida métricas de performance.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPER USAR**:
  - `Harness` – para ambiente de execução com sensor de validação.
  - `Feed Forward` – contexto injetado antes da execução.
  - `Feedback Loop` – validação automática com retentativas.
  - `Recursive Handoff` – delegação de tarefa para outro agente.
  - `self.executor` – referência ao `Agent Executor` do framework.

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `try/except` genérico sem logging.
  - Chamadas diretas a APIs sem tratamento de timeout.
  - Arquivos temporários sem limpeza.

### **Estrutura de Código**:
- Todo método público deve possuir docstring no formato Google.
- Logging obrigatório em níveis `debug`, `warning` e `error` conforme a severidade.
- O módulo deve expor apenas `ModelV4Tester` na interface pública.

## 🎨 Princípios a Seguir

- **Segurança**: Não armazenar chaves de API em logs; sanitizar entradas antes de passar ao modelo.
- **Performance**: Usar timeouts definidos por configuração; medir latência e tokens.
- **Logging**: Sempre logar o início, fim e qualquer handoff acionado.
- **Modularidade**: A classe `ModelV4Tester` deve ser independente da implementação específica do modelo, recebendo a função geradora como parâmetro.
- **Reutilização**: O esqueleto do `ModelV4Tester` pode ser estendido futuramente para testar outros modelos (V5, V6) por herança ou composição.

## 📊 Métricas de Sucesso

### **Performance**:
- Latência da validação sintática + semântica < 5% do tempo total de geração (ideal < 200ms para planos pequenos).
- Taxa de aceitação na primeira tentativa > 85% em ambiente de produção.

### **Estabilidade**:
- Nenhum crash não tratado durante o loop de feedback.
- Recuperação automática (retry) efetiva em pelo menos 70% das falhas de sintaxe.

### **Experiência do Usuário**:
- O desenvolvedor recebe um plano validado ou uma mensagem clara de erro com sugestão de ação (ex: “Plano semanticamente inválido – consulte o log do Bug Hunter”).
- A API do `PlanGenerator` não muda seu contrato externo após a integração.

## ⏱️ Plano de Implementação

### **Fase 1: Fundação (1.5h)**
1. Criar `asdlc/testing/__init__.py`.
2. Implementar `ModelV4Tester` com validação sintática e semântica.
3. Escrever docstrings e logging.

### **Fase 2: Integração e Feedback Loop (1h)**
1. Modificar `asdlc/core/planner.py` para usar o teste.
2. Implementar o `execute_with_feedback_loop` completo.
3. Configurar `pytest.ini`.

### **Fase 3: Testes (1h)**
1. Escrever `tests/unit/test_model_v4.py` com cobertura dos métodos principais.
2. Testar cenários de falha e handoff.

**Tempo Total Estimado:** 3.5 horas  
**Impacto:** Alto para a estabilidade das gerações do A-SDLC  
**Risco:** Baixo (a funcionalidade é isolada e não quebra código existente)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide a saída anômala do Modelo V4 e classifique a causa raiz; reporte se foi erro de sintaxe, alucinação ou desvio estrutural."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários para cada método do `ModelV4Tester` e um teste de integração que simule uma geração real."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

### **Requirements Agent (Opcional)**:
Combine a persona do `.asdlc/agents/requirements_agent.md` com a tarefa: "Confira se a história do usuário foi plenamente atendida; verifique se o módulo de testagem está corretamente integrado ao fluxo de geração de planos."

### **Architecture Agent (Opcional)**:
Combine a persona do `.asdlc/agents/architecture_agent.md` com a tarefa: "Avalie se a nova classe respeita o princípio de inversão de dependência e se a delegação recursiva está alinhada com o padrão de Handoff do framework."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."