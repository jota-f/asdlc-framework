# 🚀 PROMPTS & SKILLS A-SDLC - Guia de Uso

> 💡 **RECOMENDAÇÃO MODERNA (Padrão Matt Pocock)**: Se você utiliza IDEs ou agentes com suporte a Skills (Claude Code, Antigravity, Cursor, Windsurf), utilize diretamente o catálogo em `agentic_templates/skills/` (ex: `/grill-me`, `/to-story`, `/tdd`, `/implement-story`). Este diretório de prompts manuais serve como referência e fallback para chats web puros (ChatGPT/Gemini Web).

## 📁 ARQUIVOS DISPONÍVEIS

### 1. 📋 `project_description_generator.md`
**Objetivo**: Gerar descrições completas de projetos
- Transforma intenções em `PROJECT_CONTEXT.md` profissionais
- Inclui arquitetura, tech stack, padrões e métricas
- Adaptado para todos os tipos de projeto (web_api, web_frontend, mobile, desktop, cli)

### 2. 📖 `story_generator.md`
**Objetivo**: Gerar stories técnicas detalhadas
- Transforma funcionalidades em stories implementáveis
- Inclui tarefas técnicas, critérios de aceitação e estimativas
- Segue o padrão A-SDLC com agentes especializados
- **NOVO**: Inclui uso explícito das personas dos agentes

### 3. 🚀 `implementation_executor.md`
**Objetivo**: Executar implementações seguindo as personas dos agentes
- Coordena a implementação usando agentes específicos
- Documenta o processo A-SDLC passo a passo
- Garante qualidade e conformidade com padrões
- **NOVO**: Força o uso explícito das personas dos agentes

### 4. 🔍 `validation_checker.md`
**Objetivo**: Validar se implementações foram realmente executadas
- Verifica arquivos criados realmente existem
- Confirma testes implementados são funcionais
- Valida documentação foi realmente atualizada
- **NOVO**: Detecta implementações fictícias

## 🎯 COMO USAR

### **Passo 1: Escolha o Prompt**
- Use `project_description_generator.md` para **novos projetos**
- Use `story_generator.md` para **funcionalidades específicas**
- Use `implementation_executor.md` para **executar implementações**
- Use `validation_checker.md` para **validar implementações**

### **Passo 2: Copie o Conteúdo**
- Abra o arquivo `.md` desejado
- Copie todo o conteúdo
- Cole no ChatGPT, Google Gemini ou outra LLM

### **Passo 3: Forneça as Informações**
Siga o formato de entrada especificado no prompt:

**Para Projetos**:
```
Nome: [NOME_DO_PROJETO]
Tipo: [web_api/web_frontend/mobile/desktop/cli]
Intenção: [DESCRIÇÃO_DETALHADA_DA_INTENÇÃO]
```

**Para Stories**:
```
Funcionalidade: [FUNCIONALIDADE_ESPECÍFICA]
Contexto: [CONTEXTO_DO_PROJETO]
Prioridade: [ALTA/MÉDIA/BAIXA]
Dependências: [DEPENDÊNCIAS_OPCIONAIS]
```

**Para Implementações**:
```
Implemente conforme instruções do arquivo story.md seguindo as bases do PROJECT_CONTEXT.md
```

**Para Validação**:
```
Valide se a implementação da story foi realmente executada conforme o log fornecido
```

### **Passo 4: Colete o Resultado**
A LLM gerará uma descrição, story ou implementação completa seguindo o padrão A-SDLC.

## 🎨 EXEMPLOS DE USO

### **Exemplo 1: Gerando Descrição de Projeto**

**Entrada**:
```
Nome: Sistema de Gestão de Tarefas
Tipo: web_api
Intenção: Criar uma API para gerenciar tarefas de equipes, com autenticação JWT, notificações em tempo real e relatórios de produtividade. O sistema deve suportar múltiplas equipes, priorização de tarefas e integração com calendário.
```

**Saída**: Um `PROJECT_CONTEXT.md` completo com:
- Arquitetura detalhada
- Tech stack específico (FastAPI, PostgreSQL, Redis)
- Funcionalidades principais
- Padrões e métricas de qualidade

### **Exemplo 2: Gerando Story**

**Entrada**:
```
Funcionalidade: Sistema de cache inteligente para API
Contexto: Projeto web_api com FastAPI e PostgreSQL
Prioridade: Alta
Dependências: Sistema de autenticação implementado
```

**Saída**: Uma story completa com:
- Tarefas técnicas específicas
- Critérios de aceitação mensuráveis
- Exemplos de código implementáveis
- Estimativas de tempo e complexidade
- **NOVO**: Agentes responsáveis por cada tarefa

### **Exemplo 3: Executando Implementação**

**Entrada**:
```
Implemente conforme instruções do arquivo story.md seguindo as bases do PROJECT_CONTEXT.md
```

**Saída**: Implementação completa com:
- Código implementado por agentes específicos
- Documentação do processo A-SDLC
- Validações de qualidade
- README.md atualizado com contribuições dos agentes

### **Exemplo 4: Validando Implementação**

**Entrada**:
```
Valide se a implementação da story foi realmente executada conforme o log fornecido
```

**Saída**: Relatório de validação com:
- Verificação de arquivos criados
- Teste de funcionalidades implementadas
- Confirmação de testes executados
- Validação de documentação atualizada

## 🔧 CARACTERÍSTICAS DOS PROMPTS

### **✅ Profissionais**
- Seguem padrões de documentação técnica
- Incluem métricas de qualidade
- Consideram arquitetura e escalabilidade

### **✅ Específicos**
- Adaptados para cada tipo de projeto
- Incluem exemplos de código concretos
- Definem terminologia padronizada

### **✅ Completos**
- Cobrem todos os aspectos do A-SDLC
- Incluem agentes especializados
- Definem padrões obrigatórios

### **✅ Implementáveis**
- Tarefas técnicas específicas
- Critérios de aceitação mensuráveis
- Estimativas realistas

### **✅ Personas Explícitas**
- **NOVO**: Força uso explícito das personas dos agentes
- **NOVO**: Documenta contribuições específicas de cada agente
- **NOVO**: Explica processo A-SDLC no README

### **✅ Validação Real**
- **NOVO**: Detecta implementações fictícias
- **NOVO**: Verifica arquivos realmente criados
- **NOVO**: Confirma testes executados

## 🎯 BENEFÍCIOS

### **Para Desenvolvedores**:
- ✅ Documentação profissional consistente
- ✅ Padrões claros e específicos
- ✅ Estimativas realistas
- ✅ Código de alta qualidade
- ✅ **NOVO**: Processo A-SDLC bem documentado
- ✅ **NOVO**: Validação de implementações reais

### **Para Projetos**:
- ✅ Arquitetura bem definida
- ✅ Tech stack apropriado
- ✅ Métricas de qualidade
- ✅ Escalabilidade considerada
- ✅ **NOVO**: Contribuições dos agentes documentadas
- ✅ **NOVO**: Detecção de implementações falsas

### **Para Equipes**:
- ✅ Comunicação clara
- ✅ Padrões consistentes
- ✅ Critérios mensuráveis
- ✅ Processo estruturado
- ✅ **NOVO**: Visibilidade do processo A-SDLC
- ✅ **NOVO**: Confiança na qualidade das implementações

## 🚀 DICAS DE USO

### **1. Seja Específico**
- Forneça detalhes sobre a intenção
- Mencione tecnologias preferidas
- Inclua restrições ou requisitos especiais

### **2. Revise e Ajuste**
- Sempre revise a saída da LLM
- Ajuste detalhes específicos do seu projeto
- Valide estimativas e complexidade

### **3. Mantenha Consistência**
- Use a mesma terminologia em todo o projeto
- Siga os padrões definidos
- Mantenha a estrutura A-SDLC

### **4. Itere e Melhore**
- Use o resultado como base
- Adicione detalhes específicos
- Evolua conforme o projeto cresce

### **5. Use as Personas dos Agentes**
- **NOVO**: Sempre mencione qual agente está executando cada tarefa
- **NOVO**: Documente as contribuições específicas de cada agente
- **NOVO**: Explique o processo A-SDLC no README

### **6. Valide Implementações**
- **NOVO**: Use o validation_checker para verificar implementações
- **NOVO**: Confirme que arquivos foram realmente criados
- **NOVO**: Teste funcionalidades implementadas

## 📊 MELHORIAS RECENTES

### **✅ Story Generator Melhorado**:
- Inclui uso explícito das personas dos agentes
- Força documentação do processo A-SDLC
- Adiciona agente responsável por cada tarefa

### **✅ Implementation Executor Novo**:
- Prompt específico para execução de implementações
- Força uso explícito das personas dos agentes
- Documenta todo o processo A-SDLC

### **✅ Validation Checker Novo**:
- Detecta implementações fictícias
- Verifica arquivos realmente criados
- Confirma testes executados

### **✅ Qualidade Garantida**:
- Validação de critérios de aceitação
- Revisão de código por agentes específicos
- Documentação completa do processo
- Detecção de mentiras sobre implementações

## 📞 SUPORTE

Para dúvidas sobre os prompts ou sugestões de melhorias:
- Verifique a documentação do A-SDLC
- Consulte os exemplos fornecidos
- Adapte conforme suas necessidades específicas

---

**Os prompts estão otimizados para gerar documentação profissional e implementável seguindo o framework A-SDLC, com uso explícito das personas dos agentes e validação real de implementações!** 🎉 