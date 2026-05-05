---
title: "FeedbackTest"
ticket: "20260425_232806_feedbacktest"
status: "PENDENTE"
type: "user_story"
---

# Plano de Execução: FeedbackTest

## 📝 Especificações da Story

**História do Usuário:**
Como desenvolvedor do framework A-SDLC, quero uma ferramenta integrada de teste de feedback (`feedback-test`) para validar o funcionamento do loop de autocorreção (Self-Healing) dos agentes, garantindo que os sensores detectem falhas e os agentes corrijam automaticamente os erros até atingir os critérios de aceitação configurados.

## Manifesto de Arquivos (Gerado por IA)

- **CRIAR:**
  - `asdlc/commands/feedback_test.py` – Módulo do comando CLI para o teste de feedback.
  - `tests/test_feedback_command.py` – Testes unitários e de integração para o comando `feedback-test`.

- **MODIFICAR:**
  - `asdlc/cli.py` – Registrar o novo comando `feedback-test` no menu interativo e via argumentos de linha de comando.

## 🎯 Tarefas Detalhadas

---

### Tarefa 1: Implementar o comando `feedback-test` no módulo da CLI

1. **Arquivo a criar**: `asdlc/commands/feedback_test.py`
2. **Referência de Contexto**: Estrutura de comandos existente em `asdlc/cli.py` (ex: `init`, `plan`, `execute`), padrão de argumentos e integração com o engine.
3. **Ação**: Criar o módulo `FeedbackTestCommand` que é responsável por orquestrar um cenário de teste do loop de feedback.

#### 1.1 Estrutura do comando e função principal
```python
# asdlc/commands/feedback_test.py
import argparse
import logging
from asdlc.harness.feedback_loop import FeedbackLoop  # Módulo a ser referenciado (existente)
from asdlc.harness.sensor import Sensor
from asdlc.agents.code_agent import CodeAgent
from asdlc.utils.logger import setup_logger

logger = setup_logger(__name__)

class FeedbackTestCommand:
    """Comando para executar uma bateria de testes no mecanismo de feedback."""

    @staticmethod
    def register_subparser(subparsers):
        parser = subparsers.add_parser(
            "feedback-test",
            help="Executa testes automatizados do loop de feedback e autocorreção"
        )
        parser.add_argument(
            "--iterations",
            type=int,
            default=3,
            help="Número máximo de iterações de autocorreção permitidas"
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Falha se qualquer teste de feedback falhar"
        )
        return parser

    @staticmethod
    def execute(args):
        logger.info("Iniciando teste de feedback...")
        # 1. Preparar cenário: código com erro intencional
        bad_code = "def add(a, b):\n    return a - b\n"  # bug: subtrai ao invés de somar
        expected_output = "add(2, 3) == 5"

        # 2. Criar sensor que valida a saída
        sensor = Sensor(validation_lambda=lambda result: eval(expected_output) == result)

        # 3. Instanciar agente de código com feedback ativado
        agent = CodeAgent(feedback_loop_enabled=True)

        # 4. Executar loop de feedback
        feedback_loop = FeedbackLoop(max_iterations=args.iterations)
        result = feedback_loop.execute(
            agent=agent,
            code=bad_code,
            sensor=sensor,
            expected_output=expected_output
        )

        # 5. Verificar resultado final
        if result["success"]:
            logger.info("✅ Feedback test passou: autocorreção funcionou após %d iterações", result["iterations"])
            return True
        else:
            logger.error("❌ Feedback test falhou: %s", result["message"])
            if args.strict:
                exit(1)
            return False
```

#### 1.2 Integração com a CLI principal
```python
# Em asdlc/cli.py (modificação a ser feita)
from asdlc.commands.feedback_test import FeedbackTestCommand

# Dentro da função de configuração dos subparsers:
FeedbackTestCommand.register_subparser(subparsers)
```

---

### Tarefa 2: Criar testes unitários e de integração para o comando `feedback-test`

1. **Arquivo a criar**: `tests/test_feedback_command.py`
2. **Ação**: Implementar testes que simulem a execução do comando `feedback-test` com diferentes cenários de falha e sucesso, verificando se o loop de feedback se comporta como esperado.

#### 2.1 Teste de sucesso do feedback
```python
# tests/test_feedback_command.py
import pytest
from unittest.mock import patch, MagicMock
from asdlc.commands.feedback_test import FeedbackTestCommand

@patch("asdlc.commands.feedback_test.FeedbackLoop")
@patch("asdlc.commands.feedback_test.Sensor")
@patch("asdlc.commands.feedback_test.CodeAgent")
def test_feedback_test_success(mock_code_agent, mock_sensor, mock_feedback_loop):
    # Configurar mocks para simular correção após 2 iterações
    mock_loop_instance = MagicMock()
    mock_loop_instance.execute.return_value = {"success": True, "iterations": 2}
    mock_feedback_loop.return_value = mock_loop_instance

    args = MagicMock(iterations=3, strict=False)
    result = FeedbackTestCommand.execute(args)
    assert result is True
    mock_loop_instance.execute.assert_called_once()

def test_feedback_test_failure():
    # Teste com execução simulada que falha (sem correção)
    with patch("asdlc.commands.feedback_test.FeedbackLoop.execute") as mock_exec:
        mock_exec.return_value = {"success": False, "message": "Max iterations reached"}
        args = MagicMock(iterations=1, strict=False)
        result = FeedbackTestCommand.execute(args)
        assert result is False
```

#### 2.2 Teste de integração com a CLI (via chamada de processo)
```python
import subprocess
import sys

def test_cli_feedback_test_subcommand():
    """Verifica se o subcomando é reconhecido pela CLI."""
    result = subprocess.run(
        [sys.executable, "-m", "asdlc", "feedback-test", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "feedback-test" in result.stdout
```

---

## ✅ Critérios de Aceitação

- [ ] O comando `asdlc feedback-test` é reconhecido pela CLI e exibe a ajuda corretamente.
- [ ] Ao executar `asdlc feedback-test`, o teste de feedback é iniciado e, em caso de sucesso, retorna código de saída 0.
- [ ] Em cenário onde o agente não consegue corrigir o erro dentro das iterações, o comando retorna código 1 (com `--strict`).
- [ ] O teste de feedback valida explicitamente a capacidade de autocorreção de um agente de código em pelo menos um caso de exemplo (ex: bug de subtração).
- [ ] Devem existir testes automatizados (unitários e de integração) que cubram o comportamento do comando.
- [ ] O código segue os padrões de nomenclatura e logging definidos no `PROJECT_CONTEXT.md`.

## 📋 Padrões Obrigatórios a Seguir

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - **feedback-test**: nome do comando CLI.
  - **loop de feedback**, **sensor**, **autocorreção**, **iteração**: termos do domínio.
  - **CodeAgent**: referência ao agente padrão de código.
- ❌ **NUNCA USAR**:
  - **auto-fix** no lugar de autocorreção (termo oficial definido nos documentos).
  - **test-feedback** (inverter a ordem do comando).

### **Estrutura de Código**:
- Classes de comando devem seguir o padrão `BaseCommand` se existente, ou fornecer método `register_subparser` e `execute` estáticos.
- Utilizar sempre o logger configurado pelo `setup_logger` para mensagens de status.
- Nomes de variáveis em `snake_case`, classes em `PascalCase`.

## 🎨 Princípios a Seguir

- **Modularidade**: O teste de feedback deve ser autocontido em seu módulo, dependendo apenas da interface do `FeedbackLoop` e do `Sensor`.
- **Reutilização**: O comando deve ser projetado de forma que novos casos de teste possam ser adicionados facilmente (ex: via fixture).
- **Logging**: Todas as operações críticas (início do teste, cada iteração, resultado final) devem ser logadas com nível `INFO` ou `DEBUG`.
- **Segurança**: O código fornecido para teste não deve representar risco de execução arbitrária; utilizar avaliação controlada (`eval` com ambiente restrito) ou outro método seguro.
- **Performance**: O teste de feedback deve executar em menos de 2 segundos em ambiente de desenvolvimento padrão.

## 📊 Métricas de Sucesso

### **Performance**:
- Tempo de execução do comando `asdlc feedback-test` inferior a 2 segundos.
- Não mais que 3 iterações padrão para corrigir um bug simples.

### **Estabilidade**:
- 100% dos testes unitários passam (cobertura mínima de 90% do novo código).
- O comando não lança exceções não tratadas em nenhum cenário previsto.

### **Experiência do Usuário**:
- Mensagens de saída claras indicando progresso e resultado (✅/❌).
- O comando integra-se sem conflitos com outros subcomandos da CLI.

## ⏱️ Plano de Implementação

### **Fase 1: Implementação do Comando (1h)**
1. Criar `asdlc/commands/feedback_test.py` com a classe do comando.
2. Adicionar o parser do subcomando no `asdlc/cli.py`.
3. Testar manualmente via `python -m asdlc feedback-test`.

### **Fase 2: Escrita dos Testes Automatizados (1h30min)**
1. Criar `tests/test_feedback_command.py`.
2. Implementar mocks para as dependências do loop de feedback.
3. Validação de integração com a CLI real.

### **Fase 3: Ajustes e Documentação (30min)**
1. Atualizar README com a nova funcionalidade.
2. Verificar aderência aos padrões de código (black, flake8).

**Tempo Total Estimado**: 3 horas  
**Impacto**: Alto para a confiabilidade do mecanismo de feedback.  
**Risco**: Baixo (funcionalidade isolada, baixa acoplamento).

## 📋 Padrões e Instruções para Agentes

### **Code Agent (Implementação)**:
Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

### **Test Agent (Fase 2)**:
Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente os testes conforme os exemplos fornecidos, garantindo cobertura de mútliplos cenários (sucesso, falha, flags da CLI)."

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