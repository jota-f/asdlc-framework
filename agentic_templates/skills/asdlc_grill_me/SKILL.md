---
name: asdlc_grill_me
description: Skill de questionamento proativo e alinhamento socrático (Grill with Docs). O agente questiona o usuário sobre requisitos, edge cases e domínio antes de criar stories, gerando ADRs e atualizando o GLOSSARY.md.
user_command: /grill-me
invocation_mode: user_and_model
tags: [requirements, planning, domain, adr, alignment]
---

# 🔥 A-SDLC Grill Requirements Skill (`/grill-me`)

Use esta skill quando a demanda for vaga, ambígua ou introduzir novos conceitos de arquitetura e domínio. O agente atua como um interrogador técnico e Arquiteto de Domínio até que os requisitos e a linguagem estejam 100% sólidos.

## 🎯 Quando Usar (Obrigatório quando)
- A demanda introduz novas entidades, contratos de dados ou regras de negócio.
- Não há critérios de aceitação claros ou definições de edge cases.
- O escopo é ambíguo ("melhorar performance", "adicionar autenticação", "refatorar módulo").
- Há risco de colisão de termos com o domínio existente no `GLOSSARY.md`.

---

## 🧭 Procedimento Passo a Passo

### Passo 0: Injeção de Contexto & Checkpoint
Antes de responder, o agente **DEVE** verificar:
1. `.asdlc/context_checkpoint.md` (se existir, leia e remova o arquivo para evitar injeções repetidas).
2. `PROJECT_CONTEXT.md` (para arquitetura e tech stack).
3. `GLOSSARY.md` (para linguagem ubíqua e termos de domínio).
4. `stories/MEMORY.md` (para histórico de decisões anteriores).

### Passo 1: Diagnóstico de Completude & Domínio
Avalie a demanda contra o checklist:
```markdown
# Completude do Produto:
- [ ] ATOR definido? (Quem usa? Qual perfil?)
- [ ] AÇÃO clara? (O que exatamente deve acontecer?)
- [ ] BENEFÍCIO mensurável? (Qual valor entregue?)
- [ ] CONTEXTO fornecido? (Onde no sistema? Qual endpoint/componente?)
- [ ] DEPENDÊNCIAS mapeadas? (Depende de outro componente/serviço?)

# Consistência de Domínio e Arquitetura:
- [ ] COLISÃO DE TERMOS? (Os termos usados contradizem o GLOSSARY.md?)
- [ ] CARDINALIDADE ESTRUTURAL? (É 1:1, 1:N, ou N:N?)
- [ ] SEMÂNTICA DE ESTADOS? (Se há status, a transição é livre ou restrita?)
- [ ] REGRAS DE DELEÇÃO? (CASCADE, RESTRICT, SET NULL?)
```

Se todos os itens estiverem claros, prossiga para o Passo 3. Se houver lacunas, formule perguntas objetivas (Passo 2).

### Passo 2: Ciclo de Questionamento Socrático
Faça perguntas em blocos objetivos e numerados com alternativas de múltipla escolha para agilizar as respostas do usuário. Exemplo:
```text
🔥 [GRILL MODE] Detectei ambiguidades estruturais:

1. TERMOS: Você mencionou "Vídeo solto", mas nosso glossário usa "Standalone Video".
   - Devemos unificar para "Standalone Video" ou criar um conceito novo?

2. CARDINALIDADE: Qual a relação entre "Pitch" e "Vídeo"?
   - (a) 1:N (Um pitch tem vários vídeos)
   - (b) 1:1 (Cada pitch é um vídeo)

3. DELEÇÃO: Se um Pitch for deletado:
   - (a) RESTRICT (Impede deleção com vídeos)
   - (b) CASCADE (Deleta vídeos juntos)
   - (c) SET NULL (Desvincula vídeos)
```

### Passo 3: Validação & Acordos de Arquitetura
Apresente a síntese das decisões:
```markdown
🔥 [GRILL MODE] Entendimento Consolidado:
- **ATOR:** [quem] | **AÇÃO:** [o que] | **BENEFÍCIO:** [por quê]

💡 **DECISÕES DE DOMÍNIO (Atualizações para GLOSSARY.md):**
- [Termo 1]: [Definição precisa]

🏗️ **DECISÕES ARQUITETURAIS (Novos ADRs):**
- **ADR:** [Decisão estrutural, ex: Deleção RESTRICT - Trade-off: UX mais manual vs integridade de dados]
```

### Passo 4: Escrita Ativa de Artefatos (ADRs e Glossário)
Ao obter aprovação do usuário:
1. **Atualizar `GLOSSARY.md`**: Escreva ou atualize novos termos e relações.
2. **Criar ADR em `docs/adr/XXXX-titulo-da-decisao.md`**:
   - Seção Contexto, Decisão, Consequências e Trade-offs.
   - Atualize `docs/adr/LEARNING.md` com a referência do novo ADR.
3. **Encaminhar para Story**:
   - Invoque a skill `asdlc_story_generator` (`/to-story`) ou `asdlc_epic_planner` (`/to-epic`) com os requisitos 100% refinados.
