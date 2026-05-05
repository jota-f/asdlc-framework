---
title: "DebugDeepTest"
ticket: "20260425_233040_debugdeeptest"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: DebugDeepTest

## 📝 Especificações da Story

**História do Usuário:**
Implementar funcionalidade: DebugDeepTest – um comando no CLI do A-SDLC Framework que executa testes com saída detalhada de debug, incluindo logs de cada etapa, rastreamento de chamadas de agentes e métricas de performance.

## Manifesto de Arquivos (Gerado por IA)
- **CRIAR:** `src/debug_deep_test.py`
- **MODIFICAR:** `src/cli.py` (adicionar subcomando `debug-test`)
- **MODIFICAR:** `src/agent_executor.py` (adicionar suporte a modo debug)

## 🎯 Tarefas Detalhadas

### Tarefa 1: Criar módulo `debug_deep_test.py`
1. **Arquivo a criar**: `src/debug_deep_test.py`
2. **Referência de Contexto**: O módulo deve conter funções para executar testes (pytest) com flags de debug, capturar logs e gerar relatório.
3. **Ação**: Implementar classe `DebugTestRunner` com métodos para configurar logging, executar testes e exibir resultados detalhados.

#### 1.1 Implementar classe `DebugTestRunner`
```python
# src/debug_deep_test.py
import subprocess
import sys
import logging
from typing import Optional

class DebugTestRunner:
    def __init__(self, verbose: bool = False, trace_calls: bool = False):
        self.verbose = verbose
        self.trace_calls = trace_calls
        self.logger = logging.getLogger("DebugDeepTest")
        self._setup_logging()

    def _setup_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")

    def run_tests(self, test_path: str = "tests/", extra_args: Optional[list] = None) -> int:
        """Executa pytest com opções de debug."""
        cmd = [sys.executable, "-m", "pytest", test_path, "-v"]
        if self.trace_calls:
            cmd.append("--trace")
        if extra_args:
            cmd.extend(extra_args)
        self.logger.info(f"Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.logger.debug(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            self.logger.error(f"STDERR:\n{result.stderr}")
        return result.returncode
```

### Tarefa 2: Adicionar subcomando `debug-test` ao CLI
1. **Arquivo a modificar**: `src/cli.py`
2. **Ação**: Adicionar um parser para `debug-test` com argumentos `--verbose`, `--trace`, `--test-path`.

#### 2.1 Modificar `cli.py` para incluir o novo comando
```python
# src/cli.py (trecho a ser adicionado no final do arquivo ou dentro da função main)
import argparse
from src.debug_deep_test import DebugTestRunner

def add_debug_test_subparser(subparsers):
    parser = subparsers.add_parser("debug-test", help="Executa testes com saída detalhada de debug")
    parser.add_argument("--verbose", "-v", action="store_true", help="Aumenta verbosidade dos logs")
    parser.add_argument("--trace", "-t", action="store_true", help="Habilita rastreamento de chamadas")
    parser.add_argument("--test-path", default="tests/", help="Caminho para os testes (default: tests/)")
    parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="Argumentos extras para pytest")
    parser.set_defaults(func=handle_debug_test)

def handle_debug_test(args):
    runner = DebugTestRunner(verbose=args.verbose, trace_calls=args.trace)
    return runner.run_tests(test_path=args.test_path, extra_args=args.extra_args)
```

### Tarefa 3: Adicionar suporte a modo debug no `agent_executor.py`
1. **Arquivo a modificar**: `src/agent_executor.py`
2. **Ação**: Injetar configuração de debug nos agentes quando o modo debug estiver ativo.

#### 3.1 Modificar `AgentExecutor` para aceitar flag `debug`
```python
# src/agent_executor.py (trecho)
class AgentExecutor:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.logger = logging.getLogger("AgentExecutor")
        if debug:
            self.logger.setLevel(logging.DEBUG)

    def execute(self, agent_name: str, task: str):
        self.logger.debug(f"Iniciando execução do agente '{agent_name}' com tarefa: {task}")
        # ... lógica existente ...
        self.logger.debug(f"Agente '{agent_name}' concluído")
```

## ✅ Critérios de Aceitação

- [ ] O comando `asdlc debug-test` deve ser executável e aceitar os argumentos `--verbose`, `--trace`, `--test-path`.
- [ ] Ao executar `asdlc debug-test --verbose`, os logs de debug devem ser exibidos no console.
- [ ] Ao executar `asdlc debug-test --trace`, o pytest deve ser chamado com a flag `--trace` (ou equivalente) para rastrear chamadas.
- [ ] O módulo `debug_deep_test.py` deve ser importável sem erros.
- [ ] A execução de testes com falha deve retornar código de saída diferente de zero e exibir erros detalhados.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `DebugTestRunner` para a classe principal.
  - `debug-test` para o subcomando CLI.
  - `--verbose` e `--trace` para flags.
- ✅ **Nomenclatura de arquivos**: snake_case para Python.

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - Nomes genéricos como `test_runner` ou `debug`.
  - Uso de `print()` para logging; usar módulo `logging`.

### **Estrutura de Código**:
- Seguir PEP 8.
- Documentar funções com docstrings.
- Usar type hints.

## 🎨 Princípios a Seguir

- **Segurança**: Não executar comandos arbitrários do usuário; usar `subprocess` com lista de argumentos.
- **Performance**: Logging deve ser condicional para não impactar execução normal.
- **Logging**: Usar `logging.getLogger(__name__)` em cada módulo.
- **Modularidade**: `DebugTestRunner` deve ser independente do CLI.
- **Reutilização**: Permitir que outros módulos importem e usem `DebugTestRunner`.

## 📊 Métricas de Sucesso

### **Performance**:
- Tempo de execução do comando `debug-test` sem flags não deve exceder 10% do tempo normal de `pytest`.
- Logging verbose não deve adicionar mais de 5% de overhead.

### **Estabilidade**:
- O comando deve funcionar em Python 3.8+.
- Não deve quebrar comandos existentes do CLI.

### **Experiência do Usuário**:
- A saída deve ser clara e organizada, com níveis de log (INFO, DEBUG, ERROR).
- Ajuda do comando (`asdlc debug-test --help`) deve ser autoexplicativa.

## ⏱️ Plano de Implementação

### **Fase 1: Criação do módulo core** (30 min)
1. Criar `src/debug_deep_test.py` com a classe `DebugTestRunner`.
2. Implementar método `run_tests` com suporte a verbose e trace.
3. Testar manualmente a importação e execução básica.

### **Fase 2: Integração com CLI** (20 min)
1. Modificar `src/cli.py` para adicionar subcomando `debug-test`.
2. Conectar o handler ao `DebugTestRunner`.
3. Testar o comando com `--help` e execução simples.

### **Fase 3: Integração com Agent Executor** (20 min)
1. Modificar `src/agent_executor.py` para aceitar flag `debug`.
2. Adicionar logs de debug nas chamadas de agentes.
3. Testar se a flag é propagada corretamente.

**Tempo Total Estimado**: 1 hora e 10 minutos
**Impacto**: Médio para a usabilidade do framework
**Risco**: Baixo (funcionalidade isolada, sem alterações em lógica crítica)

## 📋 Padrões e Instruções para Agentes

### **Bug Hunter Agent (Fase de Diagnóstico)**:
Combine a persona do `.asdlc/agents/bug_hunter_agent.md` com a tarefa: "Valide se a implementação proposta cobre cenários de falha (ex: pytest não instalado, caminho de teste inválido) e se o tratamento de erros é adequado."

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários para `DebugTestRunner` e testes de integração para o comando CLI."

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