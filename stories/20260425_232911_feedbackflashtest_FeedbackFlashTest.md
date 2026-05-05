---
title: "FeedbackFlashTest"
ticket: "20260425_232911_feedbackflashtest"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: FeedbackFlashTest

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: FeedbackFlashTest

**Descrição Técnica:**
O FeedbackFlashTest é um módulo de verificação rápida e contínua que executa testes de sanidade no ambiente de execução do agente (Harness) imediatamente após cada ação ou delegação. Ele deve fornecer feedback instantâneo (flash) para correções automáticas (self-healing) antes que o fluxo prossiga. O foco é validação superficial mas crítica: sintaxe, imports, existência de arquivos, estrutura mínima de código e integridade de contexto.

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:** 
  - `harness/feedback_flash_test.py` (módulo principal do FeedbackFlashTest)
  - `tests/test_feedback_flash.py` (testes unitários do módulo)
- **MODIFICAR:**
  - `harness/__init__.py` (adicionar import e registrar o módulo)
  - `harness/harness_runner.py` (integrar chamada do FeedbackFlashTest no loop de execução)

## 🎯 Tarefas Detalhadas

### Tarefa 1: Criar módulo `feedback_flash_test.py`
1. **Arquivo a criar**: `harness/feedback_flash_test.py`
2. **Referência de Contexto**: O framework A-SDLC já possui conceitos de Harness, Feedback Loop, Self-Healing. O módulo deve operar como um sensor rápido.
3. **Ação**: Implementar a classe `FeedbackFlashTest` com métodos estáticos para verificação rápida de:
   - Sintaxe de código gerado (usando `compile()` ou `ast.parse()`)
   - Importações básicas existentes no ambiente isolado
   - Estrutura de diretórios mínima esperada (ex.: se um agente deve criar uma pasta `src/`, verificar se foi criada)
   - Integridade de contexto (arquivos de entrada/saída existem e não estão vazios)

#### 1.1 Implementar métodos de verificação
```python
# harness/feedback_flash_test.py
import ast
import os
import sys
from typing import List, Tuple

class FeedbackFlashTest:
    """Realiza testes rápidos de sanidade no ambiente Harness pós-ação do agente."""

    @staticmethod
    def check_syntax(code: str, language: str = "python") -> Tuple[bool, str]:
        """Verifica sintaxe de código. Retorna (sucesso, mensagem)."""
        if language == "python":
            try:
                ast.parse(code)
                return True, "Syntax OK"
            except SyntaxError as e:
                return False, f"Syntax error: {e}"
        else:
            return True, "Syntax check not supported for this language"

    @staticmethod
    def check_imports(module_names: List[str]) -> Tuple[bool, str]:
        """Verifica se módulos podem ser importados no ambiente atual."""
        missing = []
        for mod in module_names:
            try:
                __import__(mod)
            except ImportError:
                missing.append(mod)
        if missing:
            return False, f"Missing imports: {', '.join(missing)}"
        return True, "All imports available"

    @staticmethod
    def check_paths(paths: List[str]) -> Tuple[bool, str]:
        """Verifica se caminhos obrigatórios existem."""
        missing = [p for p in paths if not os.path.exists(p)]
        if missing:
            return False, f"Missing paths: {', '.join(missing)}"
        return True, "All paths exist"

    @classmethod
    def run_all(cls, context: dict) -> List[dict]:
        """Executa verificações pré-definidas baseadas no contexto. Retorna lista de resultados."""
        results = []
        # Exemplo de uso: verificar sintaxe de código gerado
        if "code" in context:
            success, msg = cls.check_syntax(context["code"])
            results.append({"check": "syntax", "success": success, "message": msg})
        # Verificação de imports esperados
        if "required_imports" in context:
            success, msg = cls.check_imports(context["required_imports"])
            results.append({"check": "imports", "success": success, "message": msg})
        # Verificação de caminhos esperados
        if "required_paths" in context:
            success, msg = cls.check_paths(context["required_paths"])
            results.append({"check": "paths", "success": success, "message": msg})
        return results
```

### Tarefa 2: Integrar FeedbackFlashTest no loop de execução do Harness
1. **Arquivo a modificar**: `harness/harness_runner.py` (ou criar se não existir, mas o manifesto já lista como modificar)
2. **Ação**: Adicionar chamada ao `FeedbackFlashTest.run_all()` após cada ação do agente, antes de prosseguir com a próxima iteração ou delegar. Se algum teste falhar, interromper o fluxo e acionar rotina de self-healing.

#### 2.1 Exemplo de integração no runner
```python
# harness/harness_runner.py (trecho a ser inserido)
from harness.feedback_flash_test import FeedbackFlashTest

class HarnessRunner:
    def __init__(self):
        self.flash_test = FeedbackFlashTest()

    def execute_agent_action(self, action_context: dict):
        # ... execução da ação ...
        # Após ação, executa feedback flash
        flash_results = self.flash_test.run_all(action_context)
        failures = [r for r in flash_results if not r["success"]]
        if failures:
            self.handle_feedback_failures(failures, action_context)
            # Pode interromper, logar ou disparar self-healing
        return flash_results

    def handle_feedback_failures(self, failures, context):
        # Implementar lógica de self-healing: registrar, tentar corrigir, etc.
        for f in failures:
            print(f" [FLASH-FAIL] {f['check']}: {f['message']}")
        # Exemplo simples: gerar relatório e parar execução
        raise RuntimeError("FeedbackFlashTest falhou - ação corrigida manualmente?")
```

### Tarefa 3: Criar testes unitários para o módulo
1. **Arquivo a criar**: `tests/test_feedback_flash.py`
2. **Ação**: Testar cada método estático e o método `run_all` com cenários de sucesso e falha.

#### 3.1 Exemplo de testes
```python
# tests/test_feedback_flash.py
import pytest
from harness.feedback_flash_test import FeedbackFlashTest

class TestFeedbackFlash:
    def test_check_syntax_valid(self):
        code = "x = 1\ny = x + 2"
        success, msg = FeedbackFlashTest.check_syntax(code)
        assert success is True
        assert "OK" in msg

    def test_check_syntax_invalid(self):
        code = "x = "
        success, msg = FeedbackFlashTest.check_syntax(code)
        assert success is False
        assert "Syntax error" in msg

    def test_check_imports_available(self):
        success, msg = FeedbackFlashTest.check_imports(["os", "sys"])
        assert success is True

    def test_check_imports_missing(self):
        success, msg = FeedbackFlashTest.check_imports(["non_existent_module"])
        assert success is False

    def test_run_all_with_context(self):
        context = {
            "code": "import os",
            "required_imports": ["os"],
            "required_paths": [".", "/nonexistent"]
        }
        results = FeedbackFlashTest.run_all(context)
        assert len(results) == 3
        syntax_result = results[0]
        assert syntax_result["success"] is True
        paths_result = results[2]
        assert paths_result["success"] is False
```

## ✅ Critérios de Aceitação

- [ ] Módulo `feedback_flash_test.py` criado com métodos `check_syntax`, `check_imports`, `check_paths`, `run_all`.
- [ ] Integração no `harness_runner.py` chamando `run_all` após cada ação agente.
- [ ] Testes unitários aprovados (100% de cobertura das funções principais).
- [ ] Falhas no flash test interrompem o fluxo e disparam rotina de self-healing (pelo menos log e exception).
- [ ] Documentação inline (docstrings) nos métodos do módulo.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `FeedbackFlashTest` – nome da classe/módulo.
  - `flash check` – para cada verificação individual.
  - `self-healing` – para correção automática.
- ❌ **NUNCA USAR**:
  - Termos genéricos como "validador" ou "verificador" sem qualificador.
  - Abreviações sem explicação (evitar `FFT` sozinho).

### **Estrutura de Código**:
- Métodos estáticos para independência.
- Retorno padronizado: `Tuple[bool, str]` para verificações individuais.
- `run_all` retorna `List[dict]` com chaves `check`, `success`, `message`.

## 🎨 Princípios a Seguir

- **Segurança**: `check_syntax` usa `ast.parse` em vez de `exec` para evitar execução de código malicioso.
- **Performance**: Verificações leves (sintaxe, existência de arquivo) – não executar análise profunda.
- **Logging**: Registrar todos os resultados de flash test com timestamp e nível WARNING para falhas.
- **Modularidade**: Cada método verifica uma única responsabilidade.
- **Reutilização**: Métodos podem ser chamados individualmente ou via `run_all`.

## 📊 Métricas de Sucesso

### **Performance**:
- Cada verificação flash deve concluir em < 100ms em ambiente de desenvolvimento.
- `run_all` com 3 verificações conclui em < 300ms.

### **Estabilidade**:
- Zero falsos positivos (não reportar falha quando tudo está correto).
- Zero falsos negativos (detectar falhas reais como sintaxe inválida).

### **Experiência do Usuário**:
- Mensagens de erro claras e acionáveis.
- Tempo de feedback < 1s após cada ação do agente.

## ⏱️ Plano de Implementação

### **Fase 1: Criação do módulo central (30 min)**
1. Criar `harness/feedback_flash_test.py` com todas as verificações.
2. Adicionar docstrings e type hints.

### **Fase 2: Integração no HarnessRunner (20 min)**
1. Modificar `harness/__init__.py` para importar `feedback_flash_test`.
2. Modificar `harness/harness_runner.py` adicionando chamada `run_all` após ação.
3. Implementar `handle_feedback_failures` mínimo (log e exception).

### **Fase 3: Testes (30 min)**
1. Criar `tests/test_feedback_flash.py` cobrindo todas as funções.
2. Executar `pytest` e validar cobertura.

**Tempo Total Estimado**: 1,5 horas
**Impacto**: Alto – estabelece fundação para feedback contínuo e self-healing.
**Risco**: Baixo – módulo isolado, integração controlada.

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide se o FeedbackFlashTest detecta corretamente sintaxe inválida e imports faltantes. Teste com códigos maliciosos (ex.: tentativa de execução com `exec`) para garantir segurança."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando `harness/feedback_flash_test.py` e modificando `harness/__init__.py` e `harness/harness_runner.py`. Siga TODOS os padrões obrigatórios e princípios. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação. Implemente testes unitários para `check_syntax`, `check_imports`, `check_paths` e `run_all`. Garanta cobertura de 100%."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com padrões obrigatórios (terminologia, estrutura), princípios (segurança, performance) e critérios de aceitação. Valide métricas de sucesso. Documente desvios."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade FeedbackFlashTest, criando `harness/feedback_flash_test.py` e modificando `harness/__init__.py` e `harness/harness_runner.py` conforme o Manifesto. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior, salvando em `tests/test_feedback_flash.py`."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."