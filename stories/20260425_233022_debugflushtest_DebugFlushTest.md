---
title: "DebugFlushTest"
ticket: "20260425_233022_debugflushtest"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: DebugFlushTest

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: DebugFlushTest

**Descrição Técnica:**
Criar um utilitário de depuração que permite "flushear" (limpar/descartar) dados de teste ou estado de depuração de forma controlada. Este utilitário será usado durante o desenvolvimento para resetar rapidamente o estado de componentes mockados, caches de teste e logs de depuração, sem precisar reiniciar o ambiente de desenvolvimento.

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:**
  - `src/utils/debug_flush.py` (Utilitário principal de DebugFlush)
  - `tests/test_debug_flush.py` (Testes unitários para o utilitário)
- **MODIFICAR:**
  - Nenhum (novo módulo)

## 🎯 Tarefas Detalhadas

### Tarefa 1: Implementar o utilitário `DebugFlush` em `src/utils/debug_flush.py`
1. **Arquivo a criar**: `src/utils/debug_flush.py`
2. **Referência de Contexto**: Este utilitário deve ser independente e não depender de outros módulos do framework A-SDLC. Deve ser importável por qualquer outro módulo.
3. **Ação**: Criar a classe `DebugFlush` com métodos estáticos para gerenciar o estado de depuração.

#### 1.1 Criar a classe `DebugFlush` com métodos estáticos
```python
# src/utils/debug_flush.py
"""
Módulo utilitário para DebugFlush.
Permite limpar/descartar dados de teste e estado de depuração de forma controlada.
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class DebugFlush:
    """
    Utilitário para gerenciar e limpar estado de depuração.
    Mantém um registro interno de componentes registrados para flush.
    """

    _registry: Dict[str, Any] = {}
    _flush_history: List[str] = []

    @classmethod
    def register(cls, name: str, component: Any) -> None:
        """
        Registra um componente para ser gerenciado pelo DebugFlush.

        Args:
            name: Nome único do componente.
            component: Referência ao componente (pode ser um objeto, dicionário, lista, etc.).
        """
        if name in cls._registry:
            logger.warning(f"Componente '{name}' já registrado. Substituindo.")
        cls._registry[name] = component
        logger.debug(f"Componente '{name}' registrado para DebugFlush.")

    @classmethod
    def unregister(cls, name: str) -> bool:
        """
        Remove um componente do registro.

        Args:
            name: Nome do componente a ser removido.

        Returns:
            True se o componente foi removido, False caso contrário.
        """
        if name in cls._registry:
            del cls._registry[name]
            logger.debug(f"Componente '{name}' removido do DebugFlush.")
            return True
        logger.warning(f"Componente '{name}' não encontrado para remoção.")
        return False

    @classmethod
    def flush(cls, name: Optional[str] = None) -> Dict[str, bool]:
        """
        Executa o flush (limpeza) de componentes registrados.

        Args:
            name: Nome específico do componente a ser flusheado. Se None, todos os componentes são flusheados.

        Returns:
            Dicionário com o resultado do flush para cada componente.
        """
        results: Dict[str, bool] = {}
        components_to_flush: Dict[str, Any] = {}

        if name:
            if name in cls._registry:
                components_to_flush[name] = cls._registry[name]
            else:
                logger.error(f"Componente '{name}' não encontrado para flush.")
                results[name] = False
                return results
        else:
            components_to_flush = dict(cls._registry)

        for comp_name, component in components_to_flush.items():
            try:
                if hasattr(component, 'flush') and callable(component.flush):
                    component.flush()
                    results[comp_name] = True
                    cls._flush_history.append(f"{comp_name}: flushed via method")
                elif isinstance(component, dict):
                    component.clear()
                    results[comp_name] = True
                    cls._flush_history.append(f"{comp_name}: flushed via dict.clear()")
                elif isinstance(component, list):
                    component.clear()
                    results[comp_name] = True
                    cls._flush_history.append(f"{comp_name}: flushed via list.clear()")
                else:
                    # Para outros tipos, tenta reatribuir um valor vazio
                    cls._registry[comp_name] = None
                    results[comp_name] = True
                    cls._flush_history.append(f"{comp_name}: flushed via reset to None")
                logger.info(f"Flush executado com sucesso para '{comp_name}'.")
            except Exception as e:
                logger.error(f"Erro ao executar flush para '{comp_name}': {e}")
                results[comp_name] = False
                cls._flush_history.append(f"{comp_name}: flush failed - {e}")

        return results

    @classmethod
    def get_registry(cls) -> Dict[str, Any]:
        """Retorna uma cópia do registro atual de componentes."""
        return dict(cls._registry)

    @classmethod
    def get_flush_history(cls) -> List[str]:
        """Retorna o histórico de operações de flush."""
        return list(cls._flush_history)

    @classmethod
    def clear_history(cls) -> None:
        """Limpa o histórico de operações de flush."""
        cls._flush_history.clear()
        logger.debug("Histórico de flush limpo.")

    @classmethod
    def reset(cls) -> None:
        """Reseta completamente o DebugFlush (limpa registro e histórico)."""
        cls._registry.clear()
        cls._flush_history.clear()
        logger.info("DebugFlush resetado completamente.")
```

### Tarefa 2: Implementar testes unitários em `tests/test_debug_flush.py`
1. **Arquivo a criar**: `tests/test_debug_flush.py`
2. **Ação**: Criar testes abrangentes para a classe `DebugFlush`.

#### 2.1 Criar testes para registro, flush e reset
```python
# tests/test_debug_flush.py
"""
Testes unitários para o módulo DebugFlush.
"""
import pytest
from src.utils.debug_flush import DebugFlush

class TestDebugFlush:
    """Suite de testes para a classe DebugFlush."""

    def setup_method(self):
        """Reseta o DebugFlush antes de cada teste."""
        DebugFlush.reset()

    def test_register_component(self):
        """Testa o registro de um componente."""
        component = {"key": "value"}
        DebugFlush.register("test_dict", component)
        registry = DebugFlush.get_registry()
        assert "test_dict" in registry
        assert registry["test_dict"] is component

    def test_register_duplicate_warning(self):
        """Testa que registrar um nome duplicado gera um warning."""
        DebugFlush.register("dup", {"a": 1})
        # Registrar novamente não deve falhar, apenas substituir
        DebugFlush.register("dup", {"b": 2})
        registry = DebugFlush.get_registry()
        assert registry["dup"] == {"b": 2}

    def test_unregister_component(self):
        """Testa a remoção de um componente."""
        DebugFlush.register("temp", [1, 2, 3])
        assert DebugFlush.unregister("temp") is True
        assert "temp" not in DebugFlush.get_registry()

    def test_unregister_nonexistent(self):
        """Testa a remoção de um componente inexistente."""
        assert DebugFlush.unregister("nonexistent") is False

    def test_flush_dict_component(self):
        """Testa o flush de um componente do tipo dicionário."""
        data = {"a": 1, "b": 2}
        DebugFlush.register("my_dict", data)
        result = DebugFlush.flush("my_dict")
        assert result["my_dict"] is True
        assert len(data) == 0

    def test_flush_list_component(self):
        """Testa o flush de um componente do tipo lista."""
        data = [1, 2, 3]
        DebugFlush.register("my_list", data)
        result = DebugFlush.flush("my_list")
        assert result["my_list"] is True
        assert len(data) == 0

    def test_flush_all_components(self):
        """Testa o flush de todos os componentes registrados."""
        dict_data = {"x": 10}
        list_data = [1, 2]
        DebugFlush.register("dict1", dict_data)
        DebugFlush.register("list1", list_data)
        results = DebugFlush.flush()  # Flush all
        assert results["dict1"] is True
        assert results["list1"] is True
        assert len(dict_data) == 0
        assert len(list_data) == 0

    def test_flush_nonexistent_component(self):
        """Testa o flush de um componente não registrado."""
        result = DebugFlush.flush("ghost")
        assert result["ghost"] is False

    def test_flush_history(self):
        """Testa o histórico de operações de flush."""
        DebugFlush.register("hist_dict", {"keep": "me"})
        DebugFlush.flush("hist_dict")
        history = DebugFlush.get_flush_history()
        assert len(history) == 1
        assert "hist_dict: flushed via dict.clear()" in history[0]

    def test_clear_history(self):
        """Testa a limpeza do histórico."""
        DebugFlush.register("temp", [])
        DebugFlush.flush("temp")
        assert len(DebugFlush.get_flush_history()) == 1
        DebugFlush.clear_history()
        assert len(DebugFlush.get_flush_history()) == 0

    def test_reset(self):
        """Testa o reset completo do DebugFlush."""
        DebugFlush.register("a", {})
        DebugFlush.register("b", [])
        DebugFlush.flush("a")
        DebugFlush.reset()
        assert len(DebugFlush.get_registry()) == 0
        assert len(DebugFlush.get_flush_history()) == 0

    def test_flush_object_with_flush_method(self):
        """Testa o flush de um objeto que possui método flush()."""
        class FlushableComponent:
            def __init__(self):
                self.data = [1, 2, 3]
                self.flushed = False

            def flush(self):
                self.data.clear()
                self.flushed = True

        component = FlushableComponent()
        DebugFlush.register("flushable", component)
        result = DebugFlush.flush("flushable")
        assert result["flushable"] is True
        assert component.flushed is True
        assert len(component.data) == 0

    def test_flush_other_types(self):
        """Testa o flush de tipos que não são dict, list ou têm método flush."""
        DebugFlush.register("int_val", 42)
        result = DebugFlush.flush("int_val")
        assert result["int_val"] is True
        # O valor deve ser resetado para None
        assert DebugFlush.get_registry()["int_val"] is None
```

## ✅ Critérios de Aceitação

- [ ] O módulo `src/utils/debug_flush.py` é criado com a classe `DebugFlush` e todos os métodos especificados.
- [ ] O módulo `tests/test_debug_flush.py` é criado com pelo menos 10 testes unitários cobrindo registro, flush, histórico e reset.
- [ ] Todos os testes passam com `pytest` sem erros.
- [ ] O código segue os padrões de logging e tratamento de erros definidos.
- [ ] O histórico de flush registra corretamente cada operação, incluindo falhas.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `DebugFlush` para a classe principal.
  - `flush` para o método de limpeza.
  - `register`/`unregister` para gerenciamento de componentes.
  - `_registry` e `_flush_history` para atributos internos.

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - Nomes genéricos como `clear`, `reset_all` (preferir `flush`).
  - Dependências de outros módulos do A-SDLC (deve ser independente).
  - Uso de `print()` para logging (usar `logging`).

### **Estrutura de Código**:
- Métodos de classe (`@classmethod`) para acesso ao estado global.
- Documentação (docstrings) em todos os métodos públicos.
- Tipagem explícita para todos os parâmetros e retornos.

## 🎨 Princípios a Seguir

- **Segurança**: Não expor o registro interno diretamente (retornar cópia em `get_registry()`).
- **Performance**: Operações de flush devem ser O(1) para um componente específico e O(n) para todos.
- **Logging**: Usar `logging` com níveis apropriados (debug, info, warning, error).
- **Modularidade**: O módulo não deve importar nada além de `logging` e `typing`.
- **Reutilização**: O `DebugFlush` pode ser usado por qualquer parte do sistema que precise de reset de estado.

## 📊 Métricas de Sucesso

### **Performance**:
- [ ] Flush de um único componente leva menos de 1ms.
- [ ] Flush de 100 componentes registrados leva menos de 10ms.
- [ ] Registro de um componente leva menos de 0.1ms.

### **Estabilidade**:
- [ ] 100% dos testes unitários passam.
- [ ] Nenhum erro não tratado é lançado durante operações normais.
- [ ] O histórico de flush nunca excede 1000 entradas (pode ser limitado futuramente).

### **Experiência do Usuário**:
- [ ] Mensagens de log claras e informativas.
- [ ] API intuitiva com nomes de métodos auto-descritivos.
- [ ] Documentação completa com exemplos de uso.

## ⏱️ Plano de Implementação

### **Fase 1: Implementação do utilitário (30 minutos)**
1. Criar o arquivo `src/utils/debug_flush.py` com a classe `DebugFlush`.
2. Implementar os métodos `register`, `unregister`, `flush`, `get_registry`, `get_flush_history`, `clear_history` e `reset`.
3. Adicionar logging e tratamento de erros.

### **Fase 2: Testes unitários (30 minutos)**
1. Criar o arquivo `tests/test_debug_flush.py`.
2. Implementar testes para todos os métodos e cenários de borda.
3. Executar `pytest` e corrigir quaisquer falhas.

**Tempo Total Estimado**: 1 hora
**Impacto**: Baixo para o sistema (módulo independente)
**Risco**: Baixo (funcionalidade isolada, sem dependências externas)

## 📋 Padrões e Instruções para Agentes

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando os arquivos `src/utils/debug_flush.py` e `tests/test_debug_flush.py`. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários conforme os exemplos fornecidos em `tests/test_debug_flush.py`. Garanta cobertura de 100% dos métodos públicos."

### **Review Agent (Fase 3)**:
Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

---

## ✅ Checklist de Execução

- [ ] **Fase 1: Escrita de Código**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando os arquivos `src/utils/debug_flush.py` e `tests/test_debug_flush.py` EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

- [ ] **Fase 2: Escrita de Testes**
  - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior. Execute `pytest tests/test_debug_flush.py -v` para validar."

- [ ] **Fase 3: Finalização**
  - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."