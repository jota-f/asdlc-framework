---
name: asdlc_architecture
description: Skill de auditoria arquitetural, limites de domínio DDD, descoberta estrutural e geração de ADRs formais (Architectural Decision Records).
user_command: /improve-architecture
invocation_mode: user_and_model
tags: [architecture, ddd, adr, boundaries, coupling, refactoring]
---

# 🏛️ A-SDLC Architecture & ADR Skill (`/improve-architecture`)

Esta skill atua como o **Architecture Agent** sênior do A-SDLC, responsável por auditar a estrutura do projeto, proteger limites de domínio (Bounded Contexts), reduzir acoplamento e registrar decisões arquiteturais formais (ADRs).

---

## 🎯 Quando Usar
- Auditoria periódica da base de código para evitar "Big Ball of Mud".
- Tomada de decisões técnicas relevantes (escolha de banco, mensageria, padrões de cache, estratégia de autenticação).
- Descoberta e documentação da arquitetura de projetos legados.

---

## 🧭 Procedimento

### 1. Auditoria de Limites e Acoplamento
Avalie o projeto com base nos princípios:
1. **Coesão e Acoplamento**: Módulos possuem responsabilidades bem delimitadas?
2. **Dependência Direcional**: O núcleo de domínio (Core Domain) depende de detalhes de infraestrutura ou frameworks? (Deveria ser o inverso - Inversão de Dependências).
3. **Linguagem Ubíqua**: O código reflete os termos do `GLOSSARY.md`?

### 2. Criação de ADR (Architectural Decision Record)
Quando uma decisão arquitetural é tomada, use esta skill para gerar o artefato:

Crie o arquivo em `docs/adr/YYYYMMDD_XXXX_[TITULO].md`:

```markdown
---
adr_id: "ADR-XXXX"
title: "[TÍTULO DA DECISÃO]"
status: "ACEITO" # PROPOSTO | ACEITO | DEPRECIADO | SUBSTITUIDO
date: "YYYY-MM-DD"
deciders: ["Architecture Agent", "Equipe de Engenharia"]
---

# ADR-XXXX: [TÍTULO DA DECISÃO]

## 📋 Contexto & Problema
[Qual é o problema ou desafio técnico que motivou esta decisão?]

## 💡 Decisão Tomada
[Qual solução/padrão foi escolhido? Quais alternativas foram descartadas?]

## ⚖️ Consequências & Trade-offs
### Impactos Positivos:
- [Benefício 1]
- [Benefício 2]

### Impactos Negativos / Custos:
- [Custo 1 / Complexidade adicionada]
- [Trade-off assumido]

## 🔗 Relação com Stories
- Relacionado à Story: `stories/YYYYMMDD_...md`
```

### 3. Atualização do Índice `docs/adr/LEARNING.md`
Sempre adicione uma linha de resumo em `docs/adr/LEARNING.md`:
`- [ADR-XXXX](docs/adr/YYYYMMDD_XXXX_titulo.md): [Resumo em 1 frase da decisão e motivação].`
