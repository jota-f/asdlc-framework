---
description: Workflow de questionamento proativo (Grill with Docs). O agente "grelha" o humano sobre requisitos e consistência de domínio antes de criar uma story, gerando ADRs e atualizando o glossário.
---

# 🔥 GRILL REQUIREMENTS (`/asdlc-grill`)

Use este comando quando a demanda é vaga, ambígua ou carece de especificidade. O agente atuará como um interrogador incansável e um Arquiteto de Domínio até que os requisitos e a linguagem estejam sólidos.

## Quando Usar (OBRIGATÓRIO quando)

- A demanda introduz novos conceitos ou entidades no sistema.
- Não há critérios de aceitação claros ou definições de edge cases.
- O escopo é ambíguo ("melhorar", "adicionar", "corrigir" sem detalhes).
- Há risco de colisão de terminologia com o domínio existente.

## Passo 0: Injeção de Contexto Obrigatória

Antes de responder ao usuário, o agente **DEVE** utilizar suas ferramentas de leitura para consultar:
1. `PROJECT_CONTEXT.md` (Para entender a arquitetura base).
2. `GLOSSARY.md` (Se não existir, o agente informará que irá criá-lo). Este arquivo guarda a linguagem ubíqua do projeto (Domain-Driven Design).
3. `stories/MEMORY.md` (Para contexto de decisões anteriores).

## Passo 1: Diagnóstico de Completude e Colisão

O agente avalia a demanda inicial contra este checklist:

```
# Completude do Produto:
- [ ] ATOR definido? (Quem usa? Qual perfil?)
- [ ] AÇÃO clara? (O que exatamente deve acontecer?)
- [ ] BENEFÍCIO mensurável? (Qual valor entregue?)
- [ ] CONTEXTO fornecido? (Onde no sistema? Qual fluxo?)
- [ ] DEPENDÊNCIAS mapeadas? (Depende de outro componente/serviço?)

# Consistência de Domínio e Arquitetura:
- [ ] COLISÃO DE TERMOS? (Os termos usados pelo usuário contradizem o GLOSSARY.md?)
- [ ] CARDINALIDADE ESTRUTURAL? (É 1:1, 1:N, ou N:N?)
- [ ] SEMÂNTICA DE ESTADOS? (Se há status, a transição é livre ou restrita?)
- [ ] DELETION RULES? (O que acontece ao deletar a entidade? CASCADE, RESTRICT, SET NULL?)
```

Se TODOS os itens estiverem preenchidos e não houver ambiguidades de domínio, sugira `/asdlc-create-story`.
Se houver lacunas, prossiga para o Passo 2.

## Passo 2: Ciclo de Questionamento

O agente faz perguntas em blocos lógicos. Exemplo:

```
🔥 [GRILL MODE] Detectei ambiguidades estruturais e de produto. Precisamos afiar isso:

1. **COLISÃO DE TERMOS**: Você mencionou "Vídeo solto", mas nosso glossário usa "Standalone Video".
   - Devemos unificar o termo para "Standalone Video" ou "Vídeo solto" é um conceito novo?

2. **CARDINALIDADE**: Qual a relação entre um "Pitch" e os "Vídeos"?
   - (a) 1:N (Um pitch tem vários vídeos)
   - (b) 1:1 (Cada pitch é um vídeo)

3. **DELEÇÃO**: Se um Pitch for deletado, o que acontece com seus vídeos?
   - (a) RESTRICT: Impede a exclusão do Pitch se houver vídeos associados.
   - (b) CASCADE: Deleta todos os vídeos junto.
   - (c) SET NULL: Os vídeos viram "Standalone Videos" sem Pitch.
```

## Passo 3: Validação & Acordos de Arquitetura

Após iterar e resolver as ambiguidades, o agente apresenta um resumo:

```
🔥 [GRILL MODE] Entendimento Consolidado:

**FUNCIONALIDADE:** [nome]
**ATOR:** [quem] | **AÇÃO:** [o que] | **BENEFÍCIO:** [por quê]

**💡 DECISÕES DE DOMÍNIO (Atualizações para o GLOSSARY.md):**
- **Pitch:** Recipiente que agrupa vídeos (1:N).
- **Pitched Video:** Um vídeo com pitch_id definido.

**🏗️ DECISÕES ARQUITETURAIS (Novos ADRs):**
- **ADR:** Exclusão de Pitches será RESTRICT (Trade-off: UX mais manual, porém evita exclusão acidental de conteúdo de alto valor).

Isso está correto? Responda:
[S] Sim, aplicar documentação e criar a story
[N] Não, preciso ajustar: [o quê]
```

## Passo 4: Escrita Ativa e Geração da Story (se aprovado)

Se o humano confirmar, o agente **NÃO APENAS** invoca a criação da story. Ele DEVE proativamente:

1. **Atualizar o Glossário:**
   - Use a ferramenta `write_to_file` ou `multi_replace_file_content` para atualizar ou criar o arquivo `GLOSSARY.md` na raiz do projeto com os novos termos.
   - ⚠️ **REGRA DE SEGURANÇA CRÍTICA:** NUNCA altere a arquitetura central, o tech stack ou os objetivos no `PROJECT_CONTEXT.md`. Toda a evolução da linguagem de negócio deve ir para o `GLOSSARY.md`.

2. **Criar ADRs:**
   - Se houver decisões estruturais não óbvias (ex: regra de deleção, escolha de tecnologia de cache), use `write_to_file` para criar um arquivo `docs/adr/XXXX-titulo-da-decisao.md` (onde XXXX é um número sequencial, ex: `0001`). O ADR deve ter seções: Contexto, Decisão e Consequências.

3. **Gerar a Story:**
   - Invoque `/asdlc-create-story` com o contexto final consolidado.

## Regras do Agente

1. **Proteja a Arquitetura:** Nunca altere as premissas do `PROJECT_CONTEXT.md`.
2. **Defenda a Linguagem Ubíqua:** Não permita que o usuário crie sinônimos (ex: User e Account) para a mesma coisa sem um debate conceitual profundo.
3. **Seja incansável**: Não aceite respostas vagas.
4. **Documente tudo ativamente**: Execute a atualização dos arquivos (`GLOSSARY.md` e `docs/adr/`) de fato, não apenas prometa que fará.
