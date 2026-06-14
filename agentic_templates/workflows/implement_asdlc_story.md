# 💻 EXECUTAR A-SDLC STORY (`/asdlc-execute`)

Este workflow automatiza o desenvolvimento, testes e validação de uma Story estruturada no backlog. Ele é **híbrido por design**: utiliza scripts locais do CLI para validações instantâneas quando disponíveis, mantendo a execução em memória como fallback para ambientes puros sem Python.

### Passos do Workflow

1. **Seleção da Story**: Especifique a Story no chat (ex: `/asdlc-execute stories/20260307_funcionalidade.md`) ou peça para a IA listar as stories pendentes do diretório.
2. **Ativação da Skill**: A IA ativará a **Skill `asdlc_implementation`**.
3. **Verificação Híbrida de Pré-Requisitos e Dependências**:
    - **SE** Python e o CLI A-SDLC estiverem disponíveis:
      O agente executa o validador via terminal (dando preferência ao executável do virtualenv `venv` ou `.venv` caso existam):
      ```bash
      # No Windows (PowerShell):
      venv\Scripts\python agentic_templates/validate_stories.py stories/[NOME_DA_STORY].md
      # No Linux/macOS:
      venv/bin/python agentic_templates/validate_stories.py stories/[NOME_DA_STORY].md
      # Fallback geral (se sem venv):
      python agentic_templates/validate_stories.py stories/[NOME_DA_STORY].md
      ```
   - **SE NÃO** (Ambiente puro de templates sem Python):
     O agente abre o arquivo `.md`, extrai o campo `depends_on` e verifica manualmente em memória se as dependências listadas estão de fato finalizadas no diretório `stories/`.
4. **Ciclo de Desenvolvimento TDD**:
   - O agente opera como **Code Agent**, abrindo e assimilando o escopo da Story.
   - Caso a Story exija criação de novos testes (ou se os existentes precisarem de atualização), o agente entra na **Red Phase** do TDD, escrevendo testes e rodando-os no terminal para garantir que falham.
    - O agente implementa a lógica necessária nos arquivos ditados no Manifesto de Arquivos (**Green Phase**), **garantindo a modularidade**: novos arquivos devem ter no máximo **300 linhas**, e adições de novos blocos complexos a arquivos legados gigantes (> 1500 linhas) devem ser evitadas ao extrair responsabilidades para novos arquivos e componentes. O agente executa e roda os testes até que passem de forma resiliente, tentando até 3 auto-correções locais antes de envolver o humano em caso de falha de teste.
5. **Fechamento e Registro de Memória**:
   - O agente executa a validação final.
   - Altera o `status` da Story para `CONCLUÍDO` (ou `Done`) e atualiza o histórico em `stories/MEMORY.md`.
