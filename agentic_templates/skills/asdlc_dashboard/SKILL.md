# 📊 Skill: A-SDLC Dashboard

Esta skill capacita o agente a gerar e interpretar o dashboard visual interativo do projeto A-SDLC diretamente do modo agentic — sem qualquer instalação ou servidor.

## 🧭 Quando Usar

- Quando o usuário pedir uma **visão geral do projeto** ("como estão as stories?", "qual o progresso?").
- Quando for necessário **apresentar o status do projeto** para stakeholders ou reviews gerenciais.
- Quando o usuário quiser **inspecionar visualmente** o backlog, o burndown ou a conformidade A-SDLC.
- Ao início de uma sessão para **reorientar o contexto** antes de executar stories.

## 🛠️ Procedimento Interno (Mental Model)

### 1. Verificar Pré-requisitos

Antes de executar, o agente DEVE confirmar:
- O projeto tem um diretório `stories/` com arquivos `.md`?
- O `python main.py dashboard --help` responde sem erro?

Se o projeto não tiver stories, informe o usuário:
```
⚠️ Nenhuma story encontrada em stories/. 
Crie stories com /asdlc-create-story antes de visualizar o dashboard.
```

### 2. Executar o Gerador

Execute o seguinte comando a partir da raiz do projeto:

```bash
python main.py dashboard --no-open
```

A flag `--no-open` evita abrir o browser automaticamente (o agente não tem UI). O arquivo é gerado em `.asdlc/dashboard/dashboard.html`.

### 3. Reportar ao Usuário

Após a geração bem-sucedida, o agente DEVE:

1. **Confirmar o caminho** do arquivo gerado.
2. **Resumir as métricas** lidas da saída do comando:
   - Total de stories / concluídas / pendentes
   - Progresso geral (% de tasks marcadas)
   - Conformidade A-SDLC (% de stories com critérios de aceitação)
3. **Instruir como abrir**: informar ao usuário que pode abrir o arquivo `.html` diretamente no browser.
4. **Sugerir próximos passos** com base nos dados (ex: stories bloqueadas, histórias sem critérios de aceitação).

### 4. Análise Proativa (Opcional mas Recomendada)

Se o agente tiver acesso de leitura às stories, DEVE analisar e reportar:

- **Stories bloqueadas**: têm `depends_on` cujas dependências ainda não estão `CONCLUÍDO`.
- **Stories sem conformidade**: não têm seção de "Critérios de Aceitação".
- **Velocity trend**: stories concluídas recentemente vs. semanas anteriores.

## 📋 Formato de Resposta Esperado

```
✅ Dashboard gerado: .asdlc/dashboard/dashboard.html

📊 Resumo do Projeto — [Nome do Projeto]
─────────────────────────────────────────
  Stories:        N total · X concluídas · Y pendentes
  Progresso:      Z% (tasks marcadas)
  Conformidade:   W% (stories com critérios de aceitação)

⚠️  Atenção:
  - Story "XXX" está bloqueada por: [dependência]
  - Story "YYY" não tem critérios de aceitação

💡 Abra o dashboard no browser:
   .asdlc/dashboard/dashboard.html
```

## 🚫 Anti-Patterns

- **Não invente métricas**: sempre leia os dados das stories reais.
- **Não abra o browser automaticamente** no modo agentic (use `--no-open`).
- **Não gere o dashboard sem stories**: informe o usuário e sugira `/asdlc-create-story`.

## 💡 Comandos Relacionados

- `/asdlc-dashboard` → Gera e resume o dashboard (este workflow).
- `/asdlc-create-story` → Cria novas stories para alimentar o dashboard.
- `/asdlc-execute` → Implementa stories pendentes para melhorar o progresso.

---
*A-SDLC Native Agentic Mode — Dashboard Skill v1.0*
