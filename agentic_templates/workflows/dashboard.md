---
description: Gera o dashboard visual interativo do projeto e resume o estado atual das stories, métricas e conformidade A-SDLC
---

# 📊 DASHBOARD A-SDLC (`/asdlc-dashboard`)

Use este comando para obter uma visão visual completa do estado do seu projeto A-SDLC. O agente gerará um arquivo HTML interativo com KPIs, burndown chart, kanban board e métricas de qualidade — **sem instalar nada**.

---

## Passos da Workflow

### 1. INJEÇÃO DE CONTEXTO (OBRIGATÓRIO)

O agente DEVE ler o `PROJECT_CONTEXT.md` para identificar o nome do projeto e o escopo atual antes de gerar o dashboard.

### 2. VERIFICAÇÃO DE PRÉ-REQUISITOS

Verifique se existem stories no diretório `stories/`:

```bash
python agentic_templates/validate_stories.py
```

- Se **não houver stories válidas**: informe o usuário e sugira `/asdlc-create-story` antes de continuar.
- Se **houver stories**: prossiga para a geração.

### 3. GERAÇÃO DO DASHBOARD

Execute o comando a partir da raiz do projeto:

```bash
python main.py dashboard --no-open
```

O dashboard será salvo em `.asdlc/dashboard/dashboard.html`.

### 4. ANÁLISE E RELATÓRIO

Após a geração, o agente DEVE:

1. **Ler as stories** de `stories/` (usando `rglob("*.md")`, excluindo `MEMORY.md`).
2. **Calcular e reportar** as métricas no chat:

```
✅ Dashboard gerado: .asdlc/dashboard/dashboard.html

📊 Resumo do Projeto — [Nome do Projeto]
─────────────────────────────────────────
  Stories:        N total · X concluídas · Y pendentes
  Progresso:      Z% das tasks marcadas como concluídas
  Conformidade:   W% das stories têm critérios de aceitação

⚠️  Pontos de Atenção:
  - [Listar stories bloqueadas por dependências não concluídas]
  - [Listar stories sem seção de Critérios de Aceitação]

💡 Para visualizar o dashboard completo, abra no browser:
   .asdlc/dashboard/dashboard.html
```

3. **Sugerir próximos passos** com base nas métricas:
   - Se progresso < 30%: sugerir `/asdlc-execute` para implementar stories pendentes.
   - Se conformidade < 80%: sugerir revisar stories sem critérios de aceitação.
   - Se houver stories bloqueadas: sugerir implementar as dependências primeiro.

### 5. ATUALIZAÇÃO OPCIONAL

Se o usuário pedir para **atualizar o dashboard** após mudanças, re-execute o passo 3. O arquivo HTML é sempre sobrescrito com os dados mais recentes.

---

## Exemplos de Uso

```
/asdlc-dashboard
→ Gera o dashboard e mostra o resumo de métricas no chat.

/asdlc-dashboard --refresh
→ Regenera o dashboard com dados atualizados.
```

---

## Integração com Outros Workflows

| Workflow | Quando usar depois |
|---|---|
| `/asdlc-create-story` | Para adicionar novas stories ao dashboard |
| `/asdlc-execute` | Para implementar stories pendentes e melhorar o progresso |
| `/asdlc-grill` | Para refinar stories sem critérios de aceitação |
| `/asdlc-bug` | Para registrar bugs descobertos durante a revisão |

---
*A-SDLC Native Agentic Mode — Dashboard Workflow v1.0*
