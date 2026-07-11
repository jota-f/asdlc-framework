---
description: Utiliza a skill do Requirements Agent para extrair contexto verbal e gravar histórias de desenvolvimento limpas
---

# 📝 CRIAR A-SDLC STORY (`/asdlc-create-story`)

Use este comando para traduzir uma ideia de negócio em um artefato tangível com escopo fechado do framework A-SDLC. O agente executará os passos abaixo.

### Passos da Workflow

1. **VALIDAÇÃO DE COMPLETUDE (OBRIGATÓRIA)**: Antes de prosseguir, o agente DEVE verificar se a demanda contém:
   - [ ] **ATOR** definido (Quem usa?)
   - [ ] **AÇÃO** clara (O que deve acontecer?)
   - [ ] **BENEFÍCIO** mensurável (Qual valor entregue?)
   
   Se QUALQUER item faltar, o agente DEVE responder:
   ```
   ⚠️ Demanda incompleta. Para criar uma story de qualidade, preciso de mais contexto.
   Use `/asdlc-grill` para um questionamento guiado, ou forneça:
   - Quem é o ator/usuário?
   - O que exatamente deve acontecer?
   - Qual o benefício esperado?
   ```
   **NÃO prossiga** até a demanda ter user story completa.

2. **SCOPE GATE (OBRIGATÓRIO)**: Com a demanda completa em mãos, avalie a dimensão do pedido **em memória** antes de qualquer I/O:

   | Sinal | Indica |
   |-------|--------|
   | Verbo de roadmap ("lançar", "construir o módulo de", "criar a plataforma de") | 🏔️ Épico |
   | Múltiplos domínios autônomos com valor independente | 🏔️ Épico |
   | 2–3 camadas técnicas num único objetivo (DB+API+UI) | 📦 Story Grande |
   | Estimativa percebida 4–8h, divisível em tracer bullets | 📦 Story Grande |
   | Objetivo único e coeso, < 4h, 1 camada dominante | 📝 Story Simples |

   - **Se 🏔️ ÉPICO**: Não prossiga. Responda: `"Este pedido tem dimensão de Épico. Vou propor a decomposição com /asdlc-create-epic."` e invoque o workflow de épico.
   - **Se 📦 STORY GRANDE**: Apresente a divisão em tracer bullets, aguarde `[S]` e depois crie cada story separadamente.
   - **Se 📝 STORY SIMPLES**: Continue para o Passo 3 sem interrupção.

3. **INJEÇÃO DE CONTEXTO (OBRIGATÓRIO)**: O agente DEVE tentar ler o `PROJECT_CONTEXT.md`, `GLOSSARY.md`, o índice de decisões `docs/adr/LEARNING.md` (se este índice não existir, consulte `docs/adr/`) e o **`BACKLOG.md`**.
   - Se o `GLOSSARY.md` **não existir** ou estiver vazio, o agente DEVE alertar o usuário ANTES de criar a story: *"⚠️ Nenhum glossário detectado. É altamente recomendado rodar o `/asdlc-grill` antes para garantir consistência de domínio."*
   - O Agente deve garantir que a Story use a **Linguagem Ubíqua** do glossário e respeite as decisões e aprendizados arquiteturais existentes.
   - **MANDATÓRIO**: O agente DEVE verificar o `BACKLOG.md` para identificar se existem Notas Mentais do Desenvolvedor ou Débitos Técnicos relacionados com a Story sendo planejada, garantindo que as ideias ou pendências sejam incorporadas e abordadas na Story atual.

4. Invoque a Skill `asdlc_story_generator` pedindo ao Agente para atuar como Product Owner Sênior.
5. Peça a IA para transformar sua demanda do prompt de chat (ex: "Criar endpoint de validação de email no backend") numa Story.
6. **MANDATÓRIO para a IA**: Utilize ferramentas de Sistema de Arquivos (como `write_to_file` ou `run_command`) e salve o Markdown gerado EXATAMENTE sob as regras da skill no diretório `stories/`.
7. **VALIDAÇÃO OBRIGATÓRIA**: A story criada deve incluir critérios de aceitação. Se não incluir, recuse e peça para corrigir antes de salvar.
8. Retorne ao humano confirmando o arquivo final com um resumo das Tarefas Técnicas identificadas!
