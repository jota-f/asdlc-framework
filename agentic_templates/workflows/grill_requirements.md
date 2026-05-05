---
description: Workflow de questionamento proativo. O agente "grelha" o humano sobre requisitos antes de criar uma story, garantindo entendimento compartilhado.
---

# 🔥 GRILL REQUIREMENTS (`/asdlc-grill`)

Use este comando quando a demanda é vaga, ambígua ou carece de especificidade. O agente atuará como um interrogador incansável até que os requisitos estejam sólidos.

## Quando Usar (OBRIGATÓRIO quando)

- A demanda não tem user story completa (ator + ação + benefício)
- Não há critérios de aceitação claros
- O escopo é ambíguo ("melhorar", "adicionar", "corrigir" sem detalhes)
- Há múltiplas interpretações possíveis

## Quando NÃO Usar

- A demanda já tem story completa e critérios de aceitação
- É uma correção menor com escopo óbvio
- O humano já forneceu documentação detalhada

## Passos da Workflow

### Passo 1: Diagnóstico de Completude

O agente avalia a demanda inicial contra este checklist:

```
- [ ] ATOR definido? (Quem usa? Qual perfil?)
- [ ] AÇÃO clara? (O que exatamente deve acontecer?)
- [ ] BENEFÍCIO mensurável? (Qual valor entregue?)
- [ ] CONTEXTO fornecido? (Onde no sistema? Qual fluxo?)
- [ ] EDGE CASES mencionados? (E se falhar? E se vazio?)
- [ ] RESTRIÇÕES explícitas? (Performance? Segurança? Compatibilidade?)
- [ ] DEPENDÊNCIAS mapeadas? (Depende de outro componente/serviço?)
```

Se TODOS os itens estiverem preenchidos, sugira `/asdlc-create-story` diretamente.
Se QUALQUER item faltar, prossiga para o Passo 2.

### Passo 2: Ciclo de Questionamento

O agente faz perguntas em blocos de 3-5 questões por vez. Exemplo:

```
🔥 [GRILL MODE] Preciso entender melhor antes de criar a story:

1. **ATOR**: Quem são os usuários que vão interagir com essa funcionalidade?
   - É um usuário final? Admin? Sistema externo?
   - Tem autenticação envolvida?

2. **CONTEXTO**: Onde no sistema isso se encaixa?
   - Qual módulo/página é afetado?
   - Existe um fluxo existente que será modificado?

3. **COMPORTAMENTO**: O que deve acontecer exatamente?
   - Qual é o resultado esperado em cada cenário?
   - E quando o input for inválido?

4. **RESTRIÇÕES**: Há limitações técnicas ou de negócio?
   - Performance máxima aceitável?
   - Compatibilidade com versões anteriores?

5. **DEPENDÊNCIAS**: Isso depende de algo que não existe ainda?
   - APIs externas? Serviços? Bibliotecas?
```

### Passo 3: Validação do Entendimento

Após 2-3 rodadas de perguntas, o agente apresenta um resumo:

```
🔥 [GRILL MODE] Entendimento Consolidado:

**FUNCIONALIDADE:** [nome]
**ATOR:** [quem]
**AÇÃO:** [o que]
**BENEFÍCIO:** [por quê]
**CONTEXTO:** [onde no sistema]
**EDGE CASES:** [lista]
**RESTRIÇÕES:** [lista]
**DEPENDÊNCIAS:** [lista]

Isso está correto? Responda:
[S] Sim, criar a story
[N] Não, preciso ajustar: [o quê]
```

### Passo 4: Geração da Story (se aprovado)

Se o humano confirmar, invoque `/asdlc-create-story` com o contexto consolidado.

## Regras do Agente

1. **Seja incansável**: Não aceite respostas vagas. Se o humano disser "melhorar a performance", pergunte "qual endpoint? qual métrica? qual baseline?"
2. **Seja específico**: Cada pergunta deve ter 2-3 opções de exemplo para guiar a resposta
3. **Seja organizado**: Apresente perguntas em blocos lógicos, não todas de uma vez
4. **Documente tudo**: Cada resposta deve ser capturada no resumo final
5. **Não implemente**: Este agente NUNCA escreve código. Apenas questiona e documenta

## Exemplo de Conversa Completa

```
Você: "/asdlc-grill Quero adicionar cache no sistema"

Agente:
🔥 [GRILL MODE] Detectei demanda vaga. Checklist de completude:
- [ ] ATOR: ❌ Não definido
- [ ] AÇÃO: ⚠️ "Adicionar cache" - qual endpoint? qual dado?
- [ ] BENEFÍCIO: ❌ Não mensurável
- [ ] CONTEXTO: ❌ Não especificado

Perguntas iniciais:

1. **O QUE cachear?** Qual endpoint ou recurso precisa de cache?
   - Ex: API de produtos, consulta de preços, listagem de pedidos

2. **POR QUÊ?** Qual problema está enfrentando?
   - Ex: Latência alta (>2s), carga no banco, custo de API externa

3. **ONDE?** Qual camada do sistema?
   - Ex: Cache no backend (Redis), cache no frontend (localStorage), CDN

Você: "O endpoint de produtos do backend fica lento, quero Redis"

Agente:
🔥 [GRILL MODE] Rodada 2 - Aprofundando:

4. **TTL**: Quanto tempo o cache deve durar?
   - Ex: 5 minutos, 1 hora, até invalidação manual

5. **INVALIDAÇÃO**: Como o cache deve ser atualizado?
   - Ex: TTL automático, invalidação por evento, manual

6. **FALLBACK**: E se o Redis estiver fora?
   - Ex: Ir direto ao banco, retornar erro, usar cache local

7. **MÉTRICA**: Como medir sucesso?
   - Ex: Reduzir latência de 2s para <200ms

Você: "TTL 5min, fallback pro banco, meta <200ms"

Agente:
🔥 [GRILL MODE] Entendimento Consolidado:

**FUNCIONALIDADE:** Cache Redis para endpoint de produtos
**ATOR:** Sistema backend (transparente ao usuário)
**AÇÃO:** Armazenar respostas em Redis com TTL de 5min
**BENEFÍCIO:** Reduzir latência de ~2s para <200ms
**CONTEXTO:** API de produtos, camada de serviço
**EDGE CASES:** Redis indisponível → fallback ao banco
**RESTRIÇÕES:** TTL 5min, não afistar consistência de dados
**DEPENDÊNCIAS:** Redis server configurado

Isso está correto?
[S] Sim, criar a story
[N] Não, preciso ajustar

Você: "S"

Agente: Story criada com sucesso: stories/20260504_cache_produtos_redis.md
```
