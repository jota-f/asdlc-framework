# 📜 PROJECT_CONTEXT.md - cli

## 1. Visão Geral do Projeto

**Nome do Projeto**: cli

**Objetivo do Projeto**: Report Generator CLI - Ferramenta CLI em Python para gerar relatórios de dados. Features: ler arquivos CSV/JSON, filtrar dados, gerar relatórios em múltiplos formatos (TXT, CSV, PDF), visualizações básicas, configuração via argumentos.

**Tipo de Aplicação**: cli

## 2. Arquitetura do Sistema

### **Componentes Principais**:
- **Backend API**: Serviços RESTful para funcionalidades principais
- **Banco de Dados**: Persistência de dados e cache
- **Integrações Externas**: APIs de terceiros conforme necessário
- **Sistema de Autenticação**: Segurança e controle de acesso

### **Fluxo de Dados**:
```
📱 Cliente → 🔐 Autenticação → 🧠 API Backend → 💾 Banco de Dados → 📤 Resposta
```

## 3. Pilha de Tecnologia (Tech Stack)

### **Backend**:
- **Framework**: FastAPI (Python) / Express.js (Node.js)
- **Banco de Dados**: PostgreSQL / MongoDB
- **Cache**: Redis
- **Autenticação**: JWT / OAuth2

### **DevOps**:
- **Containerização**: Docker
- **Orquestração**: Docker Compose / Kubernetes
- **CI/CD**: GitHub Actions / GitLab CI
- **Monitoramento**: Prometheus / Grafana

### **Qualidade**:
- **Testes**: pytest / jest
- **Linting**: black, flake8 / ESLint, Prettier
- **Documentação**: Sphinx / JSDoc

## 4. Funcionalidades Principais

### **Core Features**:
- [ ] Sistema de autenticação e autorização
- [ ] API RESTful bem documentada
- [ ] Validação de dados com Pydantic
- [ ] Tratamento robusto de erros
- [ ] Logging estruturado
- [ ] Testes automatizados

### **Integrações**:
- [ ] APIs de terceiros conforme necessário
- [ ] Sistema de notificações
- [ ] Relatórios e analytics

## 5. Padrões e Convenções Obrigatórios

### **Terminologia Padronizada**:
- ✅ **SEMPRE USAR**:
  - `api_response` para respostas de API
  - `user_authentication` para autenticação
  - `data_validation` para validação de dados
  - `error_handling` para tratamento de erros
  - `logging` para logs estruturados

### **Padrões Proibidos**:
- ❌ **NUNCA USAR**:
  - `response` - Usar `api_response`
  - `auth` - Usar `user_authentication`
  - `validate` - Usar `data_validation`
  - `try_catch` - Usar `error_handling`
  - Logs não estruturados

### **Estrutura de Código**:
- **Handlers padronizados** com try/catch
- **Logging padronizado** com emojis (🔧, ✅, ❌, 🔄)
- **Validação de dados** com Pydantic
- **Documentação de API** com OpenAPI/Swagger
- **Testes unitários** para todas as funções

## 6. Princípios Gerais de Desenvolvimento

- **Clareza e Especificidade**: Código limpo e bem documentado
- **Modularidade (SRP)**: Separação clara de responsabilidades
- **Tratamento de Erros**: Logging estruturado e tratamento robusto
- **Segurança**: Validação de inputs e autenticação adequada
- **Performance**: Otimização de consultas e cache quando necessário
- **Testabilidade**: Código testável com cobertura adequada
- **Manutenibilidade**: Código limpo e bem organizado

## 7. Métricas de Qualidade

### **Cobertura de Testes**:
- **Mínimo**: 80% de cobertura
- **Ideal**: 90%+ de cobertura
- **Tipos**: Unitários, integração, end-to-end

### **Performance**:
- **Tempo de Resposta**: < 200ms para endpoints simples
- **Throughput**: Suportar 100+ requests/segundo
- **Disponibilidade**: 99.9% uptime

### **Segurança**:
- **Validação**: 100% dos inputs validados
- **Autenticação**: Obrigatória para endpoints sensíveis
- **Logs**: Sem dados sensíveis nos logs

## 8. Estrutura de Diretórios

```
src/
├── api/              # Endpoints da API
├── services/         # Lógica de negócio
├── models/           # Modelos de dados
├── utils/            # Utilitários
├── tests/            # Testes automatizados
└── docs/             # Documentação
```

## 9. Configurações de Ambiente

### **Variáveis de Ambiente**:
- `DATABASE_URL`: URL do banco de dados
- `JWT_SECRET`: Chave secreta para JWT
- `API_KEY`: Chave da API externa
- `LOG_LEVEL`: Nível de logging

### **Configurações de Desenvolvimento**:
- **Hot Reload**: Ativo em desenvolvimento
- **Debug Mode**: Habilitado em desenvolvimento
- **Test Database**: Separado do banco principal

## 10. Próximos Passos

1. **Definir arquitetura específica** baseada no tipo de projeto
2. **Implementar funcionalidades core** conforme especificações
3. **Configurar ambiente de desenvolvimento** com todas as ferramentas
4. **Implementar testes automatizados** para garantir qualidade
5. **Documentar APIs** com OpenAPI/Swagger