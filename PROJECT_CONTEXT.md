# 📜 PROJECT_CONTEXT.md - A-SDLC Framework

## 1. Visão Geral do Projeto

**Nome do Projeto**: A-SDLC Framework

**O que é**: O A-SDLC (AI-Driven Software Development Lifecycle) é um framework inovador que integra agentes de IA especializados no ciclo de vida de desenvolvimento de software, não apenas como ferramentas de codificação, mas como participantes ativos de um processo estruturado e gerenciado.

**Objetivo do Projeto**: Criar um framework completo que permita desenvolvedores integrarem agentes de IA no desenvolvimento de software através de:
1. **Geração de Planos de Execução Detalhados**: Transformar requisitos em stories estruturadas com checklists de melhores práticas
2. **Agentes Especializados**: Utilizar personas específicas (Code, Test, Architecture, Requirements, Review) para diferentes aspectos do desenvolvimento
3. **Automação Inteligente**: Fornecer CLI híbrido e prompts profissionais para LLMs externas
4. **Processo Estruturado**: Garantir qualidade, consistência e rastreabilidade em todo o ciclo de desenvolvimento

## 2. Arquitetura do Sistema

### **Componentes Principais**:
- **Core Framework**: Lógica principal em Python com módulos especializados
- **Agentes A-SDLC**: Templates de personas para diferentes responsabilidades (Code, Test, Architecture, Requirements, Review, Bug Hunter)
- **Plan Generator**: Motor de geração de planos usando LLMs (Suporta Feature e Bug Fix)
- **Prompts Engine**: Sistema de prompts profissionais para LLMs externas
- **CLI Interface**: Interface híbrida (interativa + linha de comando)

### **Fluxo de Dados**:
```
🚀 Usuário → 📋 CLI/Interface → 🧠 Plan Generator → 🤖 Agentes A-SDLC → 📝 Stories → 💻 Implementação
```

## 3. Pilha de Tecnologia (Tech Stack)

### **Core Framework**:
- **Linguagem**: Python 3.8+
- **Framework CLI**: argparse + menu interativo
- **LLM Integration**: OpenAI API (gpt-3.5-turbo)
- **Persistência**: Sistema de arquivos (Markdown, YAML)
- **Configuração**: python-dotenv, YAML

### **Qualidade**:
- **Testes**: pytest
- **Linting**: black, flake8
- **Documentação**: Markdown, JSDoc para prompts

### **Integração**:
- **LLMs Externas**: ChatGPT, Google Gemini via prompts
- **Git**: Integração com controle de versão
- **Editores**: VS Code, qualquer editor de texto

## 4. Funcionalidades Principais

### **Core Features**:
- [ ] **Criação de Projetos**: Inicialização automática com estrutura A-SDLC
- [x] **Agentes Especializados**: 6 agentes com personas bem definidas (Adicionado Bug Hunter)
- [x] **Geração de Stories**: Transformação de requisitos em planos executáveis
- [x] **Suporte a Bugs**: Processo de RCA e Regressão integrado
- [ ] **Plan Generator**: Motor inteligente usando LLMs
- [ ] **Prompts Profissionais**: Templates para uso com LLMs externas
- [ ] **CLI Híbrido**: Interface flexível (interativa + comandos)

### **Funcionalidades Avançadas**:
- [ ] **Validação de Implementações**: Verificação se código foi realmente implementado
- [ ] **Métricas de Qualidade**: Rastreamento de conformidade com padrões
- [ ] **Templates Adaptativos**: Agentes que se adaptam ao tipo de projeto
- [ ] **Integração Git**: Hooks para aplicar A-SDLC em workflows

## 5. Padrões e Convenções Obrigatórios

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `project_context` para contexto do projeto
  - `story_template` para templates de stories
  - `agent_persona` para definição de agentes
  - `plan_generator` para geração de planos
  - `implementation_validator` para validação

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `user_story` - Usar `story_template`
  - `ai_agent` - Usar `agent_persona`
  - `code_generator` - Usar `plan_generator`
  - Implementações sem validação
  - Agentes sem personas definidas

### **Estrutura de Código**:
- **Módulos especializados** com responsabilidades únicas
- **Logging estruturado** com emojis para UX
- **Validação robusta** de inputs e outputs
- **Documentação inline** para funções complexas
- **Testes automatizados** para lógica crítica

## 6. Princípios Gerais de Desenvolvimento

- **Clareza**: Código e documentação devem ser auto-explicativos
- **Modularidade**: Separação clara de responsabilidades
- **Extensibilidade**: Facilidade para adicionar novos agentes e funcionalidades
- **Consistência**: Padrões uniformes em todo o framework
- **Qualidade**: Validação rigorosa e conformidade com A-SDLC
- **Usabilidade**: Interface intuitiva para desenvolvedores
- **Documentação**: Processo A-SDLC completamente documentado

## 7. Métricas de Qualidade

### **Cobertura de Testes**:
- **Mínimo**: 80% de cobertura
- **Ideal**: 90%+ de cobertura
- **Tipos**: Unitários, integração, validação de prompts

### **Performance**:
- **Tempo de Criação de Projeto**: < 10 segundos
- **Geração de Stories**: < 30 segundos
- **Inicialização CLI**: < 2 segundos

### **Qualidade**:
- **Conformidade A-SDLC**: 100% dos projetos gerados seguem padrões
- **Validação de Agentes**: Todas as personas bem definidas
- **Documentação**: 100% das funcionalidades documentadas

## 8. Estrutura de Diretórios

```
A-SDLC/
├── asdlc/                    # Core framework
│   ├── project_manager.py    # Gestão de projetos
│   ├── story_manager.py      # Gestão de stories
│   ├── plan_generator.py     # Geração de planos
│   ├── ui_manager.py         # Interface de usuário
│   └── llm_client.py         # Cliente LLM
├── .asdlc/                   # Configuração A-SDLC
│   └── agents/               # Agentes (Code, Test, Review, Bug Hunter, etc.)
├── prompts/                  # Templates de prompts
├── examples/                 # Projetos de exemplo
├── tests/                    # Testes automatizados
├── docs/                     # Documentação
├── main.py                   # Ponto de entrada
├── PROJECT_CONTEXT.md        # Este arquivo
└── README.md                 # Documentação principal
```

## 9. Configurações de Ambiente

### **Variáveis de Ambiente**:
- `OPENAI_API_KEY`: Chave da API OpenAI
- `ASDLC_LOG_LEVEL`: Nível de logging (DEBUG, INFO, WARNING, ERROR)
- `ASDLC_DEFAULT_PROJECT_TYPE`: Tipo padrão de projeto
- `ASDLC_LLM_MODEL`: Modelo LLM padrão

### **Configurações de Desenvolvimento**:
- **Virtual Environment**: Obrigatório para isolamento
- **Pre-commit Hooks**: Validação automática de código
- **IDE Integration**: Suporte para VS Code e outros editores

## 10. Próximos Passos

1. **Implementar validação completa** do próprio framework seguindo A-SDLC
2. **Criar stories para melhorias** usando o próprio sistema
3. **Documentar processo de contribuição** seguindo padrões A-SDLC
4. **Implementar métricas automatizadas** de conformidade
5. **Criar exemplos completos** demonstrando todas as funcionalidades
6. **Integrar com ferramentas CI/CD** para validação contínua