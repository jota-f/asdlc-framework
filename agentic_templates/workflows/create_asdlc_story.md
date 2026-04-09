---
description: Utiliza a skill do Requirements Agent para extrair contexto verbal e gravar histórias de desenvolvimento limpas
---

# 📝 CRIAR A-SDLC STORY (`/asdlc-create-story`)

Use este comando para traduzir uma ideia de negócio em um artefato tangível com escopo fechado do framework A-SDLC. O agente executará os passos abaixo.

### Passos da Workflow

1. Peça ao Agente de IA para verificar rapidamente se os repositórios têm algum contexto na raiz ou diretórios com as documentações chaves.
   - O Agente deve buscar referências cruciais como stack de banco de dados e arquitetura MVVM / Clean / Monolito.
2. Invoque a Skill `asdlc_story_generator` pedindo ao Agente para atuar como Product Owner Sênior.
3. Peça a IA para transformar sua demanda do prompt de chat (ex: "Criar endpoint de validação de email no backend") numa Story.
4. **MANDATÓRIO para a IA**: Utilize ferramentas de Sistema de Arquivos (como `write_to_file` ou `run_command`) e salve o Markdown gerado EXATAMENTE sob as regras da skill no diretório `stories/`.
5. **VALIDAÇÃO OBRIGATÓRIA**: A story criada deve incluir critérios de aceitação. Se não incluir, recuse e peça para corrigir antes de salvar.
6. Retorne ao humano confirmando o arquivo final com um resumo das Tarefas Técnicas identificadas!
