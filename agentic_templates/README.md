# 🤖 A-SDLC Agentic Mode Guide

## O que é esse diretório?
O A-SDLC Native Agentic Mode é uma alternativa de uso do framework A-SDLC projetada especificamente para desenvolvedores que já utilizam Assistentes de IA autônomos locais (como extensões MCP, Cline, Cursor, Windsurf, RooCode). 

Em vez de você (humano) rodar um CLI em Python para gerar markdowns estáticos para depois jogá-los numa IA, **esta arquitetura injeta a metodologia A-SDLC diretamente dentro da mente do seu Agente de IA**. Sem intermediários.

## 📥 Como Instalar em Qualquer Projeto

Não é necessário adicionar o pacote Python do A-SDLC. Basta instilar o "comportamento" no seu repositório:

1. Acesse o seu projeto onde deseja programar ativamente.
2. Certifique-se de que a estrutura base para diretrizes do seu agente está lá (ex: a pasta `.agents/` suportada por ferramentas de AI Software Engineering).
3. **Copie as pastas `skills/` e `workflows/` deste repositório para a sua configuração.**

**O resultado deve se parecer com isso:**
```bash
seu-aplicativo-existente/
├── .agents/
│   ├── skills/
│   │   ├── asdlc_story_generator/
│   │   └── asdlc_implementation/
│   └── workflows/
│       ├── create_asdlc_story.md
│       └── implement_asdlc_story.md
├── src/ 
└── stories/
```

## 🚀 Como Usar no Dia-a-Dia

Abra o chat da sua IDE favorita. Não crie prompts enormes do zero. Invoque as instâncias que agora você tem na máquina!

### Fase 1: Criando Histórias Baseadas em Arquitetura (Product Owner)
> **Você:** `/asdlc-create-story Preciso de uma lógica de notificação push baseada em WebSockets`

O assistente local invocará a instrução. Ele ativamente vai escanear a pasta `src/`, ler o `PROJECT_CONTEXT.md` (se você tiver), formatar o desejo como uma especificação detalhada baseada em arquivos (A-SDLC Padrão) e, sozinho, criar o arquivo `.md` na pasta `stories/` para sua aprovação.

### Fase 2: Implementando e Testando de Fato (Dev, Test & Reviewer)
Com o markdown da história criado, e após você (humano) lê-lo e ajustá-lo, você ordena:
> **Você:** `/asdlc-execute`

O assistente vai abrir o backlog. A `asdlc_implementation` skill irá forçá-lo a transitar a cognição: 
1. **Atuará como Arquiteto:** Lendo o contrato da tela ao invés de codar o que vier na cabeça.
2. **Atuará como Code Agent:** Aplicando injeções de código estritamente onde o manifesto autoriza.
3. **Atuará como Test Agent:** Chamando comandos no terminal do host de forma não vista por você até a flag de "passou" brilhar.
4. Alterará a key "status" de PENDENTE para CONCLUÍDO na história.

## Vantagens
- **Agnóstico:** Funciona perfeitamente em React, Python, Kotlin, Rust. O framework te ajuda a gerir os Agentes.
- **Rápido:** Você pula o setup Python. Apenas copia e cola `.agents/`.
- **Rastreabilidade Pessoal:** O A-SDLC te deixa ver exato o plano de implementação antes de um Agente destruir seu repositório com edições indesejadas.
