# asdlc/plan_generator.py (versão Arquiteto de Software)
import logging
from pathlib import Path
from .llm_client import call_llm
from .utils import get_project_structure

logger = logging.getLogger(__name__)

def gerar_plano_de_execucao(story_data: dict, project_root: Path) -> str:
    """
    Usa uma LLM para atuar como arquiteto e gerar um plano de execução completo.
    """
    logger.info(f"Iniciando planejamento com IA para a story: {story_data.get('title')}")

    # 1. Coletar contexto do projeto
    try:
        context_file = project_root / "PROJECT_CONTEXT.md"
        project_context = context_file.read_text(encoding='utf-8') if context_file.exists() else "Nenhum PROJECT_CONTEXT.md fornecido."
    except Exception as e:
        project_context = f"Erro ao ler PROJECT_CONTEXT.md: {e}"

    project_structure = get_project_structure(project_root)

    # 2. Construir o prompt de "Arquiteto" para a LLM
    prompt = f"""
    **PERSONA:** Você é um Arquiteto de Software Sênior e especialista no framework A-SDLC.

    **TAREFA:** Sua missão é transformar uma solicitação de alto nível em um plano de execução detalhado em Markdown. Você deve analisar a solicitação, considerar o contexto do projeto e, o mais importante, **criar um Manifesto de Arquivos específico e acionável com os arquivos de CÓDIGO FONTE necessários.**

    **REGRAS CRÍTICAS:**
    1.  Seu foco é **EXCLUSIVAMENTE** na solicitação do usuário.
    2.  O Manifesto de Arquivos deve conter **APENAS arquivos de código fonte** (ex: `.html`, `.py`, `.js`, `.css`, etc.) ou de configuração (ex: `Dockerfile`, `requirements.txt`).
    3.  **NUNCA** inclua arquivos do próprio framework A-SDLC (como `.md` da pasta `.asdlc/` ou `stories/`) no Manifesto.
    4.  **CONSIDERE O TIPO DE PROJETO:**
       - `web_frontend`: Use HTML, CSS, JavaScript (ex: `index.html`, `style.css`, `script.js`)
       - `web_api`: Use Python/Node.js (ex: `app.py`, `requirements.txt` ou `server.js`, `package.json`)
       - `web_fullstack`: Combine frontend e backend
       - `mobile`: Use React Native/Flutter (ex: `App.js`, `package.json`)
       - `desktop`: Use Electron/Python GUI (ex: `main.js`, `index.html`)
       - `cli`: Use Python/Node.js CLI (ex: `main.py`, `requirements.txt`)

    **EXEMPLOS DE BONS RESULTADOS POR TIPO:**
    ---
    **Web Frontend:**
    - Título: "Implementar relógio analógico HTML"
    - Descrição: "Criar uma página web estática que exibe um relógio analógico funcional e estilizado"
    - **Manifesto:** `index.html`, `style.css`, `script.js`
    - **Tarefas:** Estrutura HTML, design CSS, lógica JavaScript
    - **Critérios:** Design responsivo, animações suaves, JavaScript puro

    **Web API:**
    - Título: "Otimizar Cache InfluxDB com Sistema Unificado"
    - Descrição: "Implementar cache unificado por tipo de dados com rate limiting"
    - **Manifesto:** `app/services/influxdb_smart_cache.py`, `app/services/influxdb_service.py`
    - **Tarefas:** Cache unificado, rate limiting, métricas de performance
    - **Critérios:** Redução de 60% no tempo de resposta, cache hit rate > 80%

    **Mobile App:**
    - Título: "App de lista de tarefas React Native"
    - Descrição: "Aplicativo móvel para gerenciar tarefas com persistência local"
    - **Manifesto:** `App.js`, `package.json`, `components/TodoList.js`, `services/storage.js`
    - **Tarefas:** Interface React Native, persistência AsyncStorage, componentes reutilizáveis
    - **Critérios:** Interface intuitiva, persistência de dados, performance otimizada

    **Desktop App:**
    - Título: "Aplicativo desktop de gerenciamento de arquivos"
    - Descrição: "Criar aplicativo desktop para organizar e gerenciar arquivos"
    - **Manifesto:** `main.js`, `index.html`, `package.json`, `src/fileManager.js`
    - **Tarefas:** Interface Electron, gerenciamento de arquivos, UX desktop
    - **Critérios:** Interface intuitiva, performance otimizada, instalação simples

    **CLI App:**
    - Título: "CLI para gerenciamento de projetos"
    - Descrição: "Criar ferramenta de linha de comando para gerenciar projetos"
    - **Manifesto:** `main.py`, `requirements.txt`, `src/cli_commands.py`
    - **Tarefas:** Interface CLI, comandos interativos, configuração
    - **Critérios:** Interface clara, comandos intuitivos, documentação completa
    ---

    **CONTEXTO DO PROJETO ATUAL:**
    ---
    **CONSTITUIÇÃO DO PROJETO (PROJECT_CONTEXT.md):**
    {project_context}
    ---
    **ESTRUTURA DE ARQUIVOS ATUAL:**
    {project_structure}
    ---

    **SOLICITAÇÃO DO USUÁRIO ATUAL (STORY):**
    - Título: {story_data.get('title', 'N/A')}
    - Descrição: {story_data.get('description', 'N/A')}
    - Tipo de Projeto: {project_context.split('**Tipo:**')[1].split('**')[0].strip() if '**Tipo:**' in project_context else 'N/A'}

    **SUA SAÍDA:**
    Agora, com base na solicitação do usuário atual e no contexto fornecido, gere o conteúdo completo do arquivo Markdown para o plano de execução. 
    
    **IMPORTANTE:** 
    1. **ADAPTE AO TIPO DE PROJETO:**
       - `web_frontend`: Foque em HTML/CSS/JS, responsividade, UX web
       - `web_api`: Foque em Python/Node.js, segurança, documentação API
       - `web_fullstack`: Combine frontend e backend, arquitetura completa
       - `mobile`: Foque em React Native/Flutter, UX móvel, performance
       - `desktop`: Foque em Electron/Python GUI, UX desktop, instalação
       - `cli`: Foque em Python/Node.js CLI, interface de linha de comando
    
    2. **INCLUA SEMPRE** as instruções para os agentes de IA (Code Agent, Test Agent, Review Agent, etc.) na seção "🤖 Instruções para Agentes de IA".
    
    3. **SEJA ESPECÍFICO** nas tarefas, critérios de aceitação e métricas de sucesso.
    
    4. **FORNEÇA EXEMPLOS DE CÓDIGO** concretos e implementáveis nas tarefas, usando a linguagem apropriada para o tipo de projeto.
    
    5. **DEFINA PADRÕES OBRIGATÓRIOS** e princípios específicos para o tipo de projeto:
       - **Web Frontend**: Responsividade, acessibilidade, performance
       - **Web API**: Segurança, documentação, testes de integração
       - **Mobile**: UX móvel, performance, compatibilidade
       - **Desktop**: UX desktop, instalação, atualizações
       - **CLI**: Interface clara, documentação, comandos intuitivos
    
    Siga ESTRITAMENTE a estrutura de saída abaixo. Preencha TODAS as seções de forma detalhada e específica. Não adicione nenhuma outra explicação ou texto antes ou depois da sua resposta em Markdown.

    **ESTRUTURA DE SAÍDA (MARKDOWN):**
    ---
    title: "{story_data.get('title', 'N/A')}"
    ticket: "{story_data.get('id', 'N/A')}"
    status: "PENDENTE"
    ---

    # Plano de Execução: {story_data.get('title', 'N/A')}

    ## 📝 Especificações da Story

    **História do Usuário:**
    {story_data.get('description', 'N/A')}

    ## Manifesto de Arquivos (Gerado por IA)
    - **CRIAR:** [Liste EXATAMENTE os arquivos de código fonte necessários]
    - **MODIFICAR:** [Liste arquivos existentes que precisam ser alterados]

    ## 🎯 Tarefas Detalhadas

    ### Tarefa 1: [Nome da primeira tarefa]
    1. **Arquivo a criar/modificar**: [Nome do arquivo]
    2. **Referência de Contexto**: [Contexto relevante]
    3. **Ação**: [Descrição específica da ação]

    #### 1.1 [Subtarefa específica]
    ```[linguagem]
    [Código exemplo concreto e implementável]
    ```

    ### Tarefa 2: [Nome da segunda tarefa]
    1. **Arquivo a criar/modificar**: [Nome do arquivo]
    2. **Ação**: [Descrição específica da ação]

    #### 2.1 [Subtarefa específica]
    ```[linguagem]
    [Código exemplo concreto e implementável]
    ```

    ## ✅ Critérios de Aceitação

    - [ ] [Critério específico e mensurável]
    - [ ] [Critério específico e mensurável]
    - [ ] [Critério específico e mensurável]

    ## 📋 Padrões Obrigatórios a Seguir

    ### **Terminologia Padronizada**:
    - ✅ **SEMPRE USAR**:
      - [Termos específicos do projeto]
      - [Padrões de nomenclatura]

    ### **Padrões Proibidos**:
    - ❌ **NUNCA USAR**:
      - [Termos proibidos]
      - [Padrões não recomendados]

    ### **Estrutura de Código**:
    - [Padrões específicos de código]
    - [Convenções obrigatórias]

    ## 🎨 Princípios a Seguir

    - **Segurança**: [Princípio de segurança específico]
    - **Performance**: [Princípio de performance específico]
    - **Logging**: [Padrões de logging]
    - **Modularidade**: [Princípio de modularidade]
    - **Reutilização**: [Princípio de reutilização]

    ## 📊 Métricas de Sucesso

    ### **Performance**:
    - [Métrica específica e mensurável]
    - [Métrica específica e mensurável]

    ### **Estabilidade**:
    - [Métrica específica e mensurável]
    - [Métrica específica e mensurável]

    ### **Experiência do Usuário**:
    - [Métrica específica e mensurável]
    - [Métrica específica e mensurável]

    ## ⏱️ Plano de Implementação

    ### **Fase 1: [Nome da fase] ([tempo estimado])**
    1. [Passo específico]
    2. [Passo específico]
    3. [Passo específico]

    ### **Fase 2: [Nome da fase] ([tempo estimado])**
    1. [Passo específico]
    2. [Passo específico]

    **Tempo Total Estimado**: [X] horas
    **Impacto**: [Alto/Médio/Baixo] para [aspecto específico]
    **Risco**: [Alto/Médio/Baixo] ([justificativa])

    ## 🤖 Instruções para Agentes de IA

    ### **Code Agent (Fase 1)**:
    Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente EXATAMENTE as tarefas detalhadas acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga TODOS os padrões obrigatórios e princípios definidos. Use os exemplos de código fornecidos como referência."

    ### **Test Agent (Fase 2)**:
    Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie testes automatizados para validar TODOS os critérios de aceitação listados acima. Implemente testes unitários, de integração e de performance conforme as métricas de sucesso definidas."

    ### **Review Agent (Fase 3)**:
    Combine a persona do `.asdlc/agents/review_agent.md` com a tarefa: "Analise o código implementado verificando conformidade com TODOS os padrões obrigatórios, princípios e critérios de aceitação. Valide as métricas de sucesso e documente qualquer desvio."

    ### **Requirements Agent (Opcional)**:
    Combine a persona do `.asdlc/agents/requirements_agent.md` com a tarefa: "Analise se os requisitos foram completamente atendidos e se há gaps na implementação. Sugira melhorias se necessário."

    ### **Architecture Agent (Opcional)**:
    Combine a persona do `.asdlc/agents/architecture_agent.md` com a tarefa: "Valide a arquitetura implementada e verifique se está alinhada com os princípios de design definidos. Sugira otimizações arquiteturais se necessário."

    ---

    ## ✅ Checklist de Execução

    - [ ] **Fase 1: Escrita de Código**
      - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/code_agent.md` com a tarefa: "Implemente a funcionalidade descrita acima, criando e modificando os arquivos EXATAMENTE como listado no Manifesto de Arquivos. Siga as regras do `PROJECT_CONTEXT.md`."

    - [ ] **Fase 2: Escrita de Testes**
      - **Instrução para o Cursor:** Combine a persona do `.asdlc/agents/test_agent.md` com a tarefa: "Crie os testes necessários para o código gerado na fase anterior."

    - [ ] **Fase 3: Finalização**
      - **Instrução para o Cursor:** "Modifique o frontmatter deste arquivo, alterando o `status` para 'CONCLUÍDO'."
    """

    # 3. Chamar a LLM
    plano_gerado = call_llm(prompt, max_tokens=3072) # Aumentar tokens para planos complexos

    return plano_gerado 