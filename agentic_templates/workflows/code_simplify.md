# 🧹 SIMPLIFICAR E REFATORAR CÓDIGO (`/asdlc-simplify`)

Este workflow é acionado para refatorar e simplificar código recém-implementado ou legado, reduzindo a complexidade ciclomática, eliminando abstrações prematuras e mantendo 100% de aprovação na suíte de testes.

### Passos do Workflow

1. **Alvo de Simplificação**:
   Especifique o arquivo ou diretório a ser simplificado (ex: `/asdlc-simplify src/services/auth.py`) ou invoque após a conclusão de uma story com `/asdlc-execute`.

2. **Ativação da Skill**:
   A IA ativará a **Skill `asdlc_simplify`**.

3. **Inspecção de Testes Existentes (Requisito Prévio)**:
   - Antes de alterar qualquer linha de código, o agente executa a suíte de testes do projeto via terminal.
   - Se os testes já estiverem falhando **ANTES** da simplificação, o agente interrompe o workflow e avisa o usuário.

4. **Passo de Simplificação (Refactor Pass)**:
   - Extrai guard clauses para remover aninhamentos `if/else`.
   - Remove abstrações desnecessárias, imports não usados e variáveis mortas.
   - Aplica a regra de no máximo 300 linhas por arquivo novo.

5. **Re-validação Obrigatória (Green Pass)**:
   - O agente roda a suíte de testes novamente.
   - Se houver qualquer falha, o agente faz o rollback do diff problemático.

6. **Relatório de Redução**:
   - Exibe o resumo com a quantidade de linhas removidas/simplificadas e a confirmação dos testes.
