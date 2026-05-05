---
title: "RCA_Fix_Final_V3"
ticket: "20260426_010836_rca_fix_final_v3"
status: "In Progress"
type: "user_story"
---

# Plano de Execução: RCA_Fix_Final_V3

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: RCA_Fix_Final_V3 - Correções e otimizações baseadas na análise de causa raiz (RCA) do framework A-SDLC, focando em melhorias de performance, validação de feedback loop e robustez do Agent Executor.

**Contexto Técnico:**
Após análise das execuções anteriores (RCA_Fix_Final, RCA_Fix_Final_V2), foram identificados gargalos no sistema de feedback loop, falhas intermitentes na validação de conformidade e necessidade de otimização no fluxo de delegação entre agentes. Esta versão consolida todas as correções pendentes e adiciona telemetria para diagnóstico proativo.

## Manifesto de Arquivos (Gerado por IA)
- **MODIFICAR:** 
  - `asdlc/validation_checker.py`
  - `asdlc/agent_executor.py`
  - `asdlc/story_manager.py`
  - `main.py`
- **CRIAR:**
  - `asdlc/feedback_loop.py`
  - `asdlc/telemetry.py`
  - `tests/test_feedback_loop.py`
  - `tests/test_validation_checker.py`

## 🎯 Tarefas Detalhadas

### Tarefa 1: Criar Sistema de Feedback Loop Robusto
1. **Arquivo a criar/modificar**: `asdlc/feedback_loop.py` (CRIAR)
2. **Referência de Contexto**: O sistema atual de feedback no `agent_executor.py` é frágil e não persiste dados de validação entre ciclos.
3. **Ação**: Implementar classe `FeedbackLoop` com suporte a retry, persistência de métricas e integração com o Validation Checker.

#### 1.1 Implementar classe base do FeedbackLoop
```python
# asdlc/feedback_loop.py
import time
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class FeedbackMetric:
    """Métrica de feedback coletada durante execução."""
    agent_type: str
    task_id: str
    success: bool
    attempts: int
    duration_ms: float
    errors: List[str] = field(default_factory=list)
    
class FeedbackLoop:
    """Gerencia ciclo de feedback entre agentes e sensores."""
    
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 1.5
    
    def __init__(self, storage_path: Path = Path(".asdlc/feedback")):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.metrics: Dict[str, List[FeedbackMetric]] = {}
        
    def validate_and_retry(self, 
                           agent_func: callable, 
                           validator_func: callable,
                           agent_type: str,
                           task_id: str) -> Tuple[bool, any]:
        """Executa função do agente com validação e retry automático."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            start = time.time()
            try:
                result = agent_func()
                is_valid, errors = validator_func(result)
                duration = (time.time() - start) * 1000
                
                if is_valid:
                    self._record_metric(agent_type, task_id, True, attempt, duration)
                    return True, result
                else:
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.BACKOFF_FACTOR ** attempt)
                    
            except Exception as e:
                duration = (time.time() - start) * 1000
                errors = [str(e)]
                if attempt >= self.MAX_RETRIES:
                    self._record_metric(agent_type, task_id, False, attempt, duration, errors)
                    return False, None
                time.sleep(self.BACKOFF_FACTOR ** attempt)
        
        self._record_metric(agent_type, task_id, False, self.MAX_RETRIES, 0, ["Max retries exceeded"])
        return False, None
    
    def _record_metric(self, agent_type: str, task_id: str, success: bool, 
                       attempts: int, duration_ms: float, errors: List[str] = None):
        metric = FeedbackMetric(agent_type, task_id, success, attempts, duration_ms, errors or [])
        self.metrics.setdefault(agent_type, []).append(metric)
    
    def persist_metrics(self):
        """Persiste métricas para análise futura."""
        metrics_file = self.storage_path / "metrics.json"
        data = {k: [vars(m) for m in v] for k, v in self.metrics.items()}
        metrics_file.write_text(json.dumps(data, indent=2))
```

### Tarefa 2: Refatorar Validation Checker com Regras Avançadas
1. **Arquivo a criar/modificar**: `asdlc/validation_checker.py` (MODIFICAR)
2. **Ação**: Adicionar suporte a regras de validação customizadas, melhorar feedback de erros e integrar com FeedbackLoop.

#### 2.1 Adicionar sistema de regras extensível
```python
# Adicionar ao asdlc/validation_checker.py existente
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class ValidationRule:
    name: str
    check: Callable[[Any], bool]
    error_message: str
    severity: str = "error"  # error, warning, info

class EnhancedValidationChecker:
    def __init__(self):
        self._rules: Dict[str, List[ValidationRule]] = {}
        self._register_default_rules()
    
    def _register_default_rules(self):
        self.register_rule("story", ValidationRule(
            "has_manifest",
            lambda s: bool(s.get("manifest", [])),
            "Story deve conter manifesto de arquivos",
        ))
        self.register_rule("story", ValidationRule(
            "has_tasks",
            lambda s: bool(s.get("tasks", [])),
            "Story deve conter tarefas definidas",
        ))
        self.register_rule("code", ValidationRule(
            "no_asdlc_artifacts",
            lambda files: not any(f.startswith(".asdlc/") for f in files),
            "Manifesto não deve conter arquivos do framework A-SDLC",
            severity="warning"
        ))
    
    def register_rule(self, category: str, rule: ValidationRule):
        self._rules.setdefault(category, []).append(rule)
    
    def validate(self, category: str, data: Any) -> Tuple[bool, List[str]]:
        errors = []
        for rule in self._rules.get(category, []):
            if not rule.check(data):
                errors.append(f"[{rule.severity.upper()}] {rule.name}: {rule.error_message}")
        return len([e for e in errors if "ERROR" in e]) == 0, errors
```

### Tarefa 3: Adicionar Telemetria para Diagnóstico
1. **Arquivo a criar/modificar**: `asdlc/telemetry.py` (CRIAR)
2. **Ação**: Criar módulo de telemetria que coleta métricas de execução dos agentes e gera relatórios de performance.

#### 3.1 Estrutura base de telemetria
```python
# asdlc/telemetry.py
import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class AgentExecution:
    agent: str
    phase: str
    start_time: float
    end_time: float = 0
    status: str = "running"
    error: str = None
    
class TelemetryCollector:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.executions: Dict[str, List[AgentExecution]] = defaultdict(list)
        self._active: Dict[str, AgentExecution] = {}
        self._initialized = True
    
    def start_phase(self, agent: str, phase: str) -> str:
        exec_id = f"{agent}_{phase}_{time.time()}"
        self._active[exec_id] = AgentExecution(agent, phase, time.time())
        return exec_id
    
    def end_phase(self, exec_id: str, success: bool = True, error: str = None):
        if exec_id in self._active:
            exec = self._active.pop(exec_id)
            exec.end_time = time.time()
            exec.status = "success" if success else "failed"
            exec.error = error
            self.executions[f"{exec.agent}_{exec.phase}"].append(exec)
    
    def get_summary(self) -> Dict:
        return {
            phase: {
                "total": len(exs),
                "success": sum(1 for e in exs if e.status == "success"),
                "failed": sum(1 for e in exs if e.status == "failed"),
                "avg_duration_ms": sum((e.end_time - e.start_time) * 1000 for e in exs) / len(exs) if exs else 0
            }
            for phase, exs in self.executions.items()
        }
```

### Tarefa 4: Integrar Feedback Loop no Agent Executor
1. **Arquivo a criar/modificar**: `asdlc/agent_executor.py` (MODIFICAR)
2. **Ação**: Integrar o `FeedbackLoop` e `TelemetryCollector` no fluxo de execução de agentes.

#### 4.1 Atualizar método de execução principal
```python
# Modificar em asdlc/agent_executor.py
from .feedback_loop import FeedbackLoop
from .telemetry import TelemetryCollector

class AgentExecutor:
    def __init__(self, ...):
        # ... código existente ...
        self.feedback_loop = FeedbackLoop()
        self.telemetry = TelemetryCollector()
    
    def execute_agent(self, agent_type: str, task: dict) -> dict:
        exec_id = self.telemetry.start_phase(agent_type, task.get("phase", "unknown"))
        
        def agent_operation():
            return self._run_agent_in_harness(agent_type, task)
        
        def validator(result):
            checker = EnhancedValidationChecker()
            return checker.validate(agent_type, result)
        
        success, result = self.feedback_loop.validate_and_retry(
            agent_operation, validator, agent_type, task["id"]
        )
        
        if success:
            self.telemetry.end_phase(exec_id, True)
        else:
            self.telemetry.end_phase(exec_id, False, "Validation failed after retries")
        
        return {"success": success, "result": result}
```

### Tarefa 5: Atualizar CLI com Comando de Diagnóstico
1. **Arquivo a criar/modificar**: `main.py` (MODIFICAR)
2. **Ação**: Adicionar subcomando `diagnose` ao CLI para exibir métricas de telemetria.

#### 5.1 Adicionar comando diagnose
```python
# Adicionar em main.py
def add_diagnose_command(subparsers):
    diagnose_parser = subparsers.add_parser("diagnose", help="Exibir diagnóstico de execuções")
    diagnose_parser.add_argument("--format", choices=["text", "json"], default="text")
    diagnose_parser.set_defaults(func=cmd_diagnose)

def cmd_diagnose(args):
    from asdlc.telemetry import TelemetryCollector
    telemetry = TelemetryCollector()
    summary = telemetry.get_summary()
    
    if args.format == "json":
        import json
        print(json.dumps(summary, indent=2))
    else:
        print("=== Diagnóstico de Execuções ===\n")
        for phase, metrics in summary.items():
            print(f"Fase: {phase}")
            print(f"  Total: {metrics['total']}")
            print(f"  Sucessos: {metrics['success']}")
            print(f"  Falhas: {metrics['failed']}")
            print(f"  Duração Média: {metrics['avg_duration_ms']:.2f}ms\n")
    
    # Também persiste métricas do feedback loop
    from asdlc.feedback_loop import FeedbackLoop
    feedback = FeedbackLoop()
    feedback.persist_metrics()
```

### Tarefa 6: Criar Testes Automatizados
1. **Arquivo a criar/modificar**: 
   - `tests/test_feedback_loop.py` (CRIAR)
   - `tests/test_validation_checker.py` (CRIAR)
   - `tests/test_framework.py` (MODIFICAR)
2. **Ação**: Criar cobertura de testes para as novas funcionalidades.

#### 6.1 Testes do FeedbackLoop
```python
# tests/test_feedback_loop.py
import pytest
from asdlc.feedback_loop import FeedbackLoop, FeedbackMetric

def test_feedback_loop_success_on_first_try():
    loop = FeedbackLoop()
    
    def success_func():
        return {"status": "ok"}
    
    def validator(result):
        return True, []
    
    success, result = loop.validate_and_retry(success_func, validator, "test", "task-1")
    assert success
    assert result == {"status": "ok"}
    assert len(loop.metrics["test"]) == 1
    assert loop.metrics["test"][0].attempts == 1

def test_feedback_loop_retry_on_validation_failure():
    loop = FeedbackLoop()
    attempts = []
    
    def flaky_func():
        attempts.append(1)
        return {"status": "fail" if len(attempts) < 2 else "ok"}
    
    def validator(result):
        return result["status"] == "ok", ["Status not ok"] if result["status"] != "ok" else []
    
    success, result = loop.validate_and_retry(flaky_func, validator, "test", "task-2")
    assert success
    assert len(attempts) == 2
```

#### 6.2 Testes do ValidationChecker
```python
# tests/test_validation_checker.py
import pytest
from asdlc.validation_checker import EnhancedValidationChecker, ValidationRule

def test_story_validation_missing_manifest():
    checker = EnhancedValidationChecker()
    story = {"title": "Test", "tasks": [{"name": "Task 1"}]}
    is_valid, errors = checker.validate("story", story)
    assert not is_valid
    assert any("manifest" in e for e in errors)

def test_code_validation_no_asdlc_files():
    checker = EnhancedValidationChecker()
    files = ["main.py", ".asdlc/config.md", "src/app.py"]
    is_valid, warnings = checker.validate("code", files)
    assert is_valid  # apenas warning
    assert any(".asdlc/" in w for w in warnings)
```

## ✅ Critérios de Aceitação

- [x] Sistema de Feedback Loop implementado com retry automático (até 3 tentativas)
- [x] Validation Checker suporta regras extensíveis com severidade (error/warning/info)
- [x] Telemetria coleta e persiste métricas de execução dos agentes
- [x] CLI inclui comando `diagnose` para visualização de métricas
- [x] Cobertura de testes > 80% para os novos módulos (feedback_loop, telemetry, validation_checker)
- [x] Tempo de resposta do feedback loop < 100ms por tentativa (após primeira falha)
- [x] Métricas de telemetria persistidas em `.asdlc/feedback/metrics.json`

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `agent_executor` para o motor de execução
  - `harness` para ambientes isolados
  - `feedback_loop` para ciclo de validação
  - `telemetry` para coleta de métricas
  - `story` para histórias de usuário
  - `manifest` para lista de arquivos

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `agent_runner` (use `agent_executor`)
  - `sandbox` (use `harness`)
  - `log` para métricas (use `telemetry`)
  - Hardcode de paths (usar `Path` do pathlib)

### **Estrutura de Código**:
- Seguir convenção PEP 8 estritamente
- Todas as classes devem ter docstrings no formato Google
- Funções públicas devem ter type hints completos
- Usar `pathlib.Path` para manipulação de arquivos
- Configurações sensíveis via variáveis de ambiente (`.env`)

## 🎨 Princípios a Seguir

- **Segurança**: Nunca expor tokens ou credenciais em logs. Usar sanitização de dados sensíveis na telemetria.
- **Performance**: Feedback loop deve usar backoff exponencial. Operações de I/O devem ser assíncronas quando possível.
- **Logging**: Usar `logging` module com níveis apropriados (DEBUG para desenvolvimento, INFO para produção).
- **Modularidade**: Cada módulo (`feedback_loop`, `telemetry`, `validation_checker`) deve ser independente e testável isoladamente.
- **Reutilização**: Validation Checker deve ser extensível via registro de regras, não modificação de código.

## 📊 Métricas de Sucesso

### **Performance**:
- Feedback loop: validação < 50ms por tentativa (caso sucesso imediato)
- Telemetria: overhead < 5ms por coleta de métrica
- Persistência de métricas: < 200ms para 1000 métricas

### **Estabilidade**:
- Zero crashes em execuções consecutivas (teste de stress: 100 iterações)
- Retry automático resolve 95% das falhas transientes de validação
- Sistema de telemetria não afeta execução principal em caso de falha

### **Experiência do Usuário**:
- Comando `diagnose` retorna resultados em < 1 segundo
- Métricas apresentadas em formato legível (tabela texto ou JSON)
- Mensagens de erro do Validation Checker são claras e acionáveis

## ⏱️ Plano de Implementação

### **Fase 1: Fundação (2 horas)**
1. Criar módulo `feedback_loop.py` com classe base
2. Refatorar `validation_checker.py` com sistema de regras
3. Criar `telemetry.py` com coletor singleton

### **Fase 2: Integração (2 horas)**
1. Integrar FeedbackLoop e Telemetry no `agent_executor.py`
2. Atualizar `story_manager.py` para usar novo Validation Checker
3. Adicionar comando `diagnose` ao `main.py`

### **Fase 3: Testes e Documentação (1 hora)**
1. Criar testes unitários em `tests/test_feedback_loop.py`
2. Criar testes do validador em `tests/test_validation_checker.py`
3. Atualizar testes de integração em `tests/test_framework.py`

**Tempo Total Estimado**: 5 horas
**Impacto**: Alto para confiabilidade do framework
**Risco**: Baixo (módulos novos, sem alteração de APIs existentes)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide se a implementação do FeedbackLoop resolve os problemas de falha intermitente na validação. Verifique se o retry automático cobre casos de timeout e erro de rede."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários, de integração e de performance conforme as métricas de sucesso definidas."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."