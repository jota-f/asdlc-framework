# A-SDLC Tool Guide

Este guia detalha as tools disponíveis no A-SDLC Agentic Mode e como otimizar seu uso para reduzir tokens.

## Tools Principais (Sempre no Contexto)

Estas tools devem estar SEMPRE disponíveis no contexto do agente:

| Tool | Prioridade | Descrição |
|------|------------|-----------|
| `read_file` | HIGH | Ler conteúdo de arquivo |
| `write_file` | HIGH | Criar/sobrescrever arquivo |
| `edit_file` | HIGH | Editar arquivo existente |
| `glob_search` | HIGH | Buscar arquivos por padrão |
| `grep_search` | HIGH | Buscar conteúdo em arquivos |

## Tools Secundárias (Sob Demanda)

Estas tools têm `defer_loading: true` e devem ser carregadas apenas quando necessário:

| Tool | Quando Usar | Exemplo de Invocação |
|------|--------------|---------------------|
| `list_directory` | Precisa ver estrutura de pastas | Ao iniciar novo projeto |
| `run_terminal` | Precisa executar comandos | Rodar testes, build |
| `search_codebase` | Busca avançada por múltiplos arquivos | Quando glob não basta |
| `get_file_info` | Precisa de metadados (tamanho, data) | Raramente necessário |

## Padrão Tool Search Tool

### Por Que Usar?

Manter muitas tool definitions no contexto consome tokens desnecessariamente. O padrão Tool Search Tool permite:

- **Reducão de até 85%** em token usage em definitions
- Manter acesso completo ao toolkit
- Carregar tools apenas quando necessário

### Como Implementar

1. **No system prompt**, defina apenas as 5 tools principais
2. **Para tools secundárias**, use padrão de loading condicional:

```
# Tool Search Tool Pattern
Quando precisar de [FUNCIONALIDADE]:
1. Primeiro, verifique se [TOOL_PRINCIPAL] resolve
2. Se não, invoque "load_tool: [FERRAMENTA_SECUNDARIA]"
3. A tool será carregada temporariamente no contexto
```

### Exemplo Prático

```markdown
# Sistema de Tools

## Tools de Alta Prioridade (Sempre no contexto)
- read_file: Ler arquivos
- write_file: Criar arquivos  
- edit_file: Modificar arquivos
- glob_search: Buscar por padrões
- grep_search: Buscar conteúdo

## Tools de Baixa Prioridade (Carregar sob demanda)
Para usar list_directory, run_terminal, search_codebase:
→ Simply mention which tool you need and it will be loaded
```

## Otimização de Token por Tool

| Cenário | Tokens Típicos | Dica |
|---------|----------------|------|
| 5 tools principais | ~500 tokens | Manter sempre |
| 20+ tools | ~2000+ tokens | Usar Tool Search |
| Cada tool adicional | +100 tokens | Ser seletivo |

## Recomendações Práticas

1. **Prefira glob_search a list_directory** - mais específico
2. **Use grep_search com padrão exato** - menos ruído
3. **Evite run_terminal se read_file basta** - reduz contexto
4. **Cache o PROJECT_CONTEXT** - não releia a cada ação

## Exemplo de Conversation Otimizada

```
Bom: "Liste os arquivos TypeScript em src/components"
Melhor: "Use glob_search para encontrar *.tsx em src/components"
```

A segunda forma é mais eficiente porque:
- Especifica exatamente qual tool usar
- Reduz ambiguidade
- Ocupa menos tokens no historial
