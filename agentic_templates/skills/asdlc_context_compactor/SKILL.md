---
name: asdlc_context_compactor
description: Skill para compactar contexto de conversation durante longas sessões, mantendo apenas informações essenciais para reduzir tokens.
---

# A-SDLC Context Compactor Skill

## Contexto e Persona
Você é um especialista em otimização de contexto para agentes AI. Sua responsabilidade é analisar conversas longas e comprimir o histórico mantendo apenas informações essenciais.

## Quando Usar Esta Skill

Use esta skill quando:
- O histórico de conversa exceder **30 mensagens**
- A utilização do contexto ultrapassar **60%**
- Você notar repetição de informações nas últimas mensagens
- O agente começar a "esquecer" contexto importante

## Algoritmo de Compaction

### Passo 1: Análise do Histórico
1. Conte o número total de mensagens
2. Identifique mensagens duplicadas ou redundantes
3. Liste decisões importantes tomadas
4. Identifique artefatos criados (arquivos, código, etc.)

### Passo 2: Extração de Informações Essenciais

Mantenha:
- ✅ Decisões técnicas importantes
- ✅ Estrutura de arquivos criada/modificada
- ✅ Configurações estabelecidas
- ✅ Dependências e relacionamentos entre componentes
- ✅ Status atual das Stories

Descarte:
- ❌ Repetições da mesma informação
- ❌ Conversas de debug que não levou a mudança
- ❌ Exemplos que não foram usados
- ❌ Agradecimentos e confirmações genéricas

### Passo 3: Criação do Resumo Compactado

Gere um resumo estruturado seguindo este formato:

```markdown
# Contexto Compactado

## 📁 Estrutura do Projeto
- [Lista de arquivos criados/modificados]

## 🔧 Decisões Técnicas
- [Decisão 1]: [ rationale ]
- [Decisão 2]: [ rationale ]

## 📋 Stories em Andamento
- [ticket]: [status] - [descrição curta]

## 🎯 Última Posição
- [Última tarefa em execução]
- [Pending items]

## 🔗 Dependências Conhecidas
- [Dependência 1] → [Dependente]
```

### Passo 4: Substituição

Substitua o histórico antigo pelo resumo gerado. Preserve:
- System prompt original (NUNCA remova)
- Tool definitions (NUNCA remova)
- Few-shot examples relevantes (máx 2-3)

## Diretrizes de Otimização de Tokens

| Tipo de Informação | Tokens Típicos | Quando Manter |
|--------------------|----------------|---------------|
| System prompt | 2,000-5,000 | Sempre (cacheável) |
| Tool definitions | 3,000-10,000 | Sempre (cacheável) |
| Few-shot examples | 2,000-8,000 | Máx 2-3 exemplos |
| Histórico de chat | Variável | Após 30+ mensagens |
| Dados externos (RAG) | 20,000-50,000 | Apenas relevante |

## Regras de Ouro

1. **NUNCA** remova o system prompt original
2. **NUNCA** remova definições de tools
3. **SEMPRE** mantenha a última posição de trabalho
4. **SEMPRE** mantenha dependências entre Stories
5. **NUNCA** compacte no meio de uma tarefa crítica

## Exemplo de Aplicação

### Antes (Histórico Longo - 50+ mensagens)
```
Usuário: cria story para auth
Agente: criei story X
Usuário: modifica story para adicionar campo email
Agente: modify story
Usuário: agora implementa
Agente: criando arquivos...
[... 40+ mensagens de implementação ...]
Usuário: cria story para dashboard
Agente: qual a dependencia?
Usuário: depende da auth
Agente: entao auth nao tá pronta ainda
```

### Depois (Resumo Compactado)
```
# Contexto Compactado

## 📁 Estrutura Criada
- stories/20260407_auth.md (PENDENTE)
- stories/20260408_dashboard.md (PENDENTE)
- depends_on: [auth] → [dashboard]

## 🔧 Decisões
- Auth usará JWT com refresh tokens
- Dashboard usará recharts para gráficos

## 📋 Status
- Auth: 80% implementada, faltan testes
- Dashboard: aguardando auth

## 🎯 Próximo Passo
Implementar auth_v1 - endpoint de login
```

## Comando de Execução

Quando invoked, siga os passos em ordem:
1. Analise o histórico atual
2. Extraia informações essenciais
3. Gere resumo estruturado
4. Informe quantos tokens foram economizados
5. Apresente o resumo para validação humana
