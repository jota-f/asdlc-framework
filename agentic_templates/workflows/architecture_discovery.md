---
description: Workflow para descoberta arquitetural. Use para discutir modelagem, padrões e decisões técnicas ANTES de criar uma story formal.
---

# 🏗️ DESCOBERTA ARQUITETURAL (`/asdlc-architecture`)

Use este comando para perguntas livres de arquitetura e modelagem. Ideal para quando você **ainda não sabe** como implementar algo ou quer validar ideias antes de criar uma story.

## Quando Usar

- Precisa decidir a melhor estrutura de banco de dados
- Quer entender padrões de design recomendados
- Tem dúvida sobre qual biblioteca/framework usar
- Quer discutir alternativas antes de se comprometer

## Como Usar

```
Você: "/asdlc-architecture Quero adicionar um sistema de notificações. Qual a melhor abordagem para WebSocket vs Server-Sent Events?"
```

## Passos da Workflow

1. O agente atua como **Architecture Agent** do A-SDLC
2. Analisa o `PROJECT_CONTEXT.md` do projeto (se existir)
3. Considera a stack tecnológica atual
4. Apresenta opções de design com prós e contras
5. Faz perguntas de clarificação se necessário
6. **NÃO cria arquivos ainda** - apenas discute e recomenda

## O que o Architecture Agent Considera

- **Escalabilidade**: A solução cresce com o projeto?
- **Complexidade**: O custo de manutenção vale a pena?
- **Stack atual**: Usa bibliotecas já presentes no projeto?
- **Dependências**: Quais novas dependências serão necessárias?
- **Testabilidade**: Fácil de testar?

## Exemplo de Conversa

```
Você: "/asdlc-architecture Preciso de auth no meu app. Tenho um backend Python FastAPI e frontend React."

Architecture Agent:
"Opções para autenticação:

1. **JWT puro** (recomendado para este stack)
   - Prós: Sem sessão, stateless, popular
   - Contras: Tokens no cliente precisam de cuidado
   
2. **Session + Cookies**
   - Prós: Mais seguro por padrão, fácil revoke
   - Contras: Estado no servidor, scaling horizontal precisa de Redis

3. **OAuth2/OIDC (Auth0, Firebase)**
   - Prós: Menos código próprio, security gerenciada
   - Contras: Custo, vendor lock-in

Para FastAPI + React, recomendo JWT com refresh tokens.
Quer que eu detalhe a implementação?"
```

## Pós-Discussão

Após a discussão arquitetural, você pode:
- Pedir para criar a story: `/asdlc-create-story Implementar auth com JWT`
- Pedir para refinar a arquitetura: mais detalhes sobre uma opção
- Abandonar a ideia se não Makes sense

## Integração com Stories

A recomendação arquitetural pode ser copiada para a story como "Contexto da Decisão" no campo Regras Ocultas.
