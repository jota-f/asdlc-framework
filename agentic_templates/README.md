# 🤖 A-SDLC Agentic Mode Guide (v2.0.0)

## O que é esse diretório?
O A-SDLC Native Agentic Mode é uma alternativa de uso do framework A-SDLC projetada especificamente para desenvolvedores que já utilizam Assistentes de IA autônomos locais (como extensões MCP, Cline, Cursor, Windsurf, RooCode). 

Em vez de você (humano) rodar um CLI em Python para gerar markdowns estáticos para depois jogá-los numa IA, **esta arquitetura injeta a metodologia A-SDLC diretamente dentro da mente do seu Agente de IA**. Sem intermediários.

## 📥 Como Instalar em Qualquer Projeto

Não é necessário adicionar o pacote Python do A-SDLC. Basta instalar o "comportamento" no seu repositório:

1. Acesse o seu projeto onde deseja programar ativamente.
2. Certifique-se de que a estrutura base para diretrizes do seu agente está lá (ex: a pasta `.agents/` suportada por ferramentas de AI Software Engineering).
3. **Copie a pasta `agentic_templates/` deste repositório para a raiz do seu projeto.**
4. Renomeie para `.agents/` se sua ferramenta suportar (opcional).

**O resultado deve se parecer com isso:**
```bash
seu-projeto/
├── .agents/              # (opcional - renomeie agentic_templates/)
│   ├── skills/
│   ├── workflows/
│   └── stories/
├── src/
└── stories/              # Suas stories geradas
```

---

## 🚀 Quick Start

### Passo 1: Copie a pasta
```bash
cp -r agentic_templates/ seu-projeto/
```

### Passo 2: Pronto! Use os comandos no chat da IDE

| Comando | Quando Usar |
|---------|-------------|
| `/asdlc-architecture` | Perguntas de arquitetura e modelagem (antes de criar story) |
| `/asdlc-plan` | Analisar escopo grande e quebrar em múltiplas stories |
| `/asdlc-create-story` | Criar uma story formal após ter contexto definido |
| `/asdlc-execute` | Executar/implementar uma story pendente |

---

## 📋 Workflow Completo

### Fase 1: Descoberta (Opcional)
> **Você:** `/asdlc-architecture Quero adicionar WebSocket para notificações. WebSocket ou Server-Sent Events?`

O agente atua como Architecture Agent, discute opções e recomenda a melhor abordagem. Não cria arquivos ainda.

### Fase 2: Planejamento (Opcional)
> **Você:** `/asdlc-plan Preciso de auth completo: login, registro, recuperação de senha, OAuthGoogle`

O agente analisa o escopo e cria múltiplas stories sequenciais se necessário:
- Auth v1: Core + Database
- Auth v2: UI (Login/Registro)
- Auth v3: API Endpoints
- Auth v4: OAuth

### Fase 3: Criação da Story
> **Você:** `/asdlc-create-story Sistema de notificações via WebSocket`

O agente cria a story em `stories/` seguindo o template A-SDLC.

### Fase 4: Implementação
> **Você:** `/asdlc-execute`

O agente executa a story: cria arquivos, roda testes, marca como CONCLUÍDO e atualiza o índice.

---

## 🆕 What's New (v2.0.0)

| Feature | Descrição |
|---------|-----------|
| `/asdlc-architecture` | Workflow de descoberta arquitetural |
| `/asdlc-plan` | Análise de escopo com quebra automática em sub-stories |
| `depends_on` | Sistema de dependências entre stories |
| `MEMORY.md` | Memória consolidada do projeto (otimiza tokens) |
| `Context Compactor` | Skill para reduzir tokens em sessões longas |
| `TOOL_GUIDE.md` | Guia de otimização de tools |

---

## 🔗 Sistema de Dependências

Stories podem ter dependências. Use o campo `depends_on`:

```yaml
---
title: "Dashboard com Gráficos"
ticket: "20260408_DASH"
status: "PENDENTE"
depends_on: ["20260407_NOTIFY"]
---
```

**Regras:**
- Story só executa se todas dependências = `CONCLUÍDO`
- Agente verifica automaticamente
- Referencie pelo ticket

---

## 📊 Versionamento de Stories

Para features grandes, divida em partes:

```
YYYYMMDD_feature_v1.md  # Core
YYYYMMDD_feature_v2.md  # UI  
YYYYMMDD_feature_v3.md  # Integração
```

Quebra recomendada: Core → UI → Integração → Tests

---

## ⚡ Otimização de Tokens

O Agentic Mode minimiza tokens automaticamente:

### Estrutura de Contexto

| Elemento | % do Contexto |
|----------|---------------|
| System prompt | 1-2.5% |
| Tool definitions | 1.5-5% |
| Few-shot | 1-4% |
| Story atual | 25% |
| Histórico | 50% |

### Dicas

1. **MEMORY.md primeiro** - visão geral da memória sem iterar stories
2. **PROJECT_CONTEXT** - inclua apenas seção relevante
3. **Context Compactor** - invoque após 30+ mensagens
4. **Cache local** - guarde convenções do projeto

---

## 📁 Estrutura de Arquivos

```
agentic_templates/
├── README.md                    # Este arquivo
├── README_EN.md                 # Versão em inglês
├── TOOL_GUIDE.md               # Guia de otimização
├── validate_stories.py         # Validador de stories
├── skills/
│   ├── asdlc_story_generator/  # Criar stories
│   ├── asdlc_implementation/  # Executar stories
│   └── asdlc_context_compactor/ # Compactar contexto
├── workflows/
│   ├── architecture_discovery.md
│   ├── scope_analysis.md
│   ├── create_asdlc_story.md
│   └── implement_asdlc_story.md
└── stories/
    ├── MEMORY.md                # Memória do projeto
    └── exemplo/                # Exemplos
```

---

## 💡 Dicas de Uso

### Sempre leia primeiro:
```bash
stories/MEMORY.md  # ~200 tokens vs 5000+ de todas stories
```

### Para perguntas de arquitetura:
```
/asdlc-architecture Qual a melhor abordagem para auth em React + Node?
```

### Para escopos grandes:
```
/asdlc-plan Preciso de um sistema completo de e-commerce
```

---

## ⚙️ Requisitos

- IDE com suporte a agentes AI (Cursor, Windsurf, Cline, RooCode)
- Pasta `.agents/` ou equivalente suportada pela IDE
- Não requer Python ou dependências

---

## 📖 Mais Informações

- **[stories/exemplo/README.md](stories/exemplo/README.md)** - Guia completo de versionamento
- **[TOOL_GUIDE.md](TOOL_GUIDE.md)** - Otimização de tools e tokens
- **[stories/MEMORY.md](stories/MEMORY.md)** - Memória do projeto (gerado automaticamente)
