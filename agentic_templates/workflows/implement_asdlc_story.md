---
description: Delega a um Agente de Inteligência Artificial o desenvolvimento, teste e fechamento tático de uma A-SDLC Story pré-montada de acordo com o padrão estrito.
---

# 💻 EXECUTAR A-SDLC STORY (`/asdlc-execute`)

Este workflow é ideal para automatizar a materialização de arquitetura e lógica técnica documentados em um backlog de Story.

### Passos da Workflow

1. Peça à IA para listar os arquivos mais recentes da pasta `/stories/` pendentes. Alternativamente, especifique a Story no chat: `/asdlc-execute 20260307_funcionalidade.md`.
2. A IA ativará a **Skill `asdlc_implementation`**.
3. Pela Skill, o Agente abrirá a Story, lerá as especificações para assimilar o contexto.
4. O Agente começará a operar como **Code Agent**, criando as pastas/arquivos ditados no `.md`.
5. Com a edição terminada, a IA passa para a Role de **Test Agent**, lendo a Subseção dos Critérios de Aceitação e validando usando ferramentas de build via terminal. O agente NÃO perguntará ajuda inicial para falhas lógicas, deve tentar 3 auto-correções antes de envolver o humano.
6. A Inteligência reabrirá o documento da Story e alterará os parâmetros para CONCLUÍDO e confirmará via sistema de chat a finalização tática do seu pedido!
