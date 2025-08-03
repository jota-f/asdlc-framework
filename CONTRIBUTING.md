# 🤝 Guia de Contribuição - A-SDLC Framework

Obrigado por considerar contribuir com o A-SDLC Framework! Este documento fornece diretrizes para contribuições que seguem os próprios princípios do framework.

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Processo A-SDLC para Contribuições](#processo-a-sdlc-para-contribuições)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Reportando Bugs](#reportando-bugs)
- [Solicitando Features](#solicitando-features)

## 🚀 Como Contribuir

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Git** para controle de versão
3. **Conta no GitHub** para fork e pull requests
4. **Conhecimento básico** do framework A-SDLC

### Setup Inicial

1. **Fork o repositório:**
   ```bash
   # No GitHub, clique em "Fork" no repositório principal
   ```

2. **Clone seu fork:**
   ```bash
   git clone https://github.com/seu-usuario/asdlc-framework.git
   cd asdlc-framework
   ```

3. **Configure o ambiente:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

4. **Configure o upstream:**
   ```bash
   git remote add upstream https://github.com/original-owner/asdlc-framework.git
   ```

## 🔄 Processo A-SDLC para Contribuições

Seguindo os princípios do próprio framework, cada contribuição deve seguir este processo:

### 1. 📝 Criar uma "Story" de Contribuição

Use o próprio A-SDLC para planejar sua contribuição:

```bash
# No diretório do framework
python main.py
# Escolha: 3 (Criar/Implementar Story)
# Descreva sua contribuição como uma story
```

**Exemplo de Story:**
```
Título: Melhorar validação de entrada no CLI
Descrição: Implementar validação mais robusta para argumentos de linha de comando
Tipo: cli
Critérios de Aceitação:
- Validar todos os argumentos obrigatórios
- Fornecer mensagens de erro claras
- Manter compatibilidade com versões anteriores
```

### 2. 🏗️ Seguir as Personas dos Agentes

Durante o desenvolvimento, considere as 5 personas do A-SDLC:

- **Requirements Agent** 📋 - Defina claramente o que será implementado
- **Architecture Agent** 🏗️ - Planeje a estrutura e tecnologias
- **Code Agent** 💻 - Implemente código limpo e eficiente
- **Test Agent** 🧪 - Crie testes abrangentes
- **Review Agent** 👀 - Revise qualidade e conformidade

### 3. 📋 Checklist de Contribuição

Antes de submeter, verifique:

- [ ] **Story criada** e documentada
- [ ] **Código implementado** seguindo padrões
- [ ] **Testes escritos** e passando
- [ ] **Documentação atualizada**
- [ ] **Conformidade A-SDLC** verificada

## 📝 Padrões de Código

### Python

- **PEP 8** - Estilo de código Python
- **Type hints** - Para funções públicas
- **Docstrings** - Documentação inline
- **Nomes descritivos** - Variáveis e funções

```python
def create_project_structure(project_name: str, project_type: str) -> bool:
    """
    Cria a estrutura de diretórios para um novo projeto A-SDLC.
    
    Args:
        project_name: Nome do projeto
        project_type: Tipo do projeto (web_frontend, cli, etc.)
        
    Returns:
        bool: True se criado com sucesso, False caso contrário
    """
    # Implementação aqui
    pass
```

### Estrutura de Arquivos

- **Módulos organizados** em `asdlc/`
- **Testes** em `tests/`
- **Exemplos** em `examples/`
- **Documentação** em arquivos `.md`

### Commits

Use mensagens de commit claras e descritivas:

```bash
# ✅ Bom
git commit -m "feat: adicionar validação de argumentos CLI"

# ❌ Evitar
git commit -m "fix stuff"
```

**Prefixo recomendado:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `test:` - Testes
- `refactor:` - Refatoração
- `style:` - Formatação
- `perf:` - Melhoria de performance

## 🧪 Testes

### Executando Testes

```bash
# Testes unitários
python -m pytest tests/

# Testes com cobertura
python -m pytest tests/ --cov=asdlc

# Testes específicos
python -m pytest tests/test_project_manager.py
```

### Escrevendo Testes

- **Testes unitários** para cada função
- **Testes de integração** para workflows
- **Testes de conformidade** A-SDLC
- **Cobertura mínima** de 80%

```python
def test_create_project_structure():
    """Testa criação de estrutura de projeto."""
    result = create_project_structure("test-project", "cli")
    assert result is True
    assert os.path.exists("test-project")
    # Limpeza
    shutil.rmtree("test-project")
```

## 📚 Documentação

### Atualizando Documentação

1. **README.md** - Para mudanças principais
2. **PROJECT_CONTEXT.md** - Para contexto técnico
3. **Docstrings** - Para funções e classes
4. **Exemplos** - Para novas funcionalidades

### Padrões de Documentação

- **Clareza** - Linguagem simples e direta
- **Exemplos** - Código prático
- **Estrutura** - Organização lógica
- **Atualização** - Manter sincronizado com código

## 🐛 Reportando Bugs

### Template de Bug Report

```markdown
**Descrição do Bug:**
[Descrição clara e concisa]

**Passos para Reproduzir:**
1. Vá para '...'
2. Clique em '...'
3. Role para baixo até '...'
4. Veja o erro

**Comportamento Esperado:**
[O que deveria acontecer]

**Comportamento Atual:**
[O que está acontecendo]

**Screenshots:**
[Se aplicável]

**Ambiente:**
- OS: [Windows/macOS/Linux]
- Python: [versão]
- A-SDLC: [versão]

**Informações Adicionais:**
[Qualquer contexto adicional]
```

## 💡 Solicitando Features

### Template de Feature Request

```markdown
**Problema que a feature resolve:**
[Descrição do problema ou necessidade]

**Solução proposta:**
[Descrição da solução]

**Alternativas consideradas:**
[Outras soluções que foram consideradas]

**Contexto adicional:**
[Qualquer informação adicional]
```

## 🔄 Processo de Pull Request

### 1. Preparação

```bash
# Crie uma branch para sua feature
git checkout -b feature/nova-funcionalidade

# Desenvolva sua contribuição
# ... código ...

# Teste suas mudanças
python -m pytest tests/
```

### 2. Commit e Push

```bash
# Adicione suas mudanças
git add .

# Faça commit com mensagem descritiva
git commit -m "feat: adicionar nova funcionalidade X"

# Push para seu fork
git push origin feature/nova-funcionalidade
```

### 3. Pull Request

1. **Vá para GitHub** e clique em "New Pull Request"
2. **Selecione sua branch** como source
3. **Preencha o template** de PR:

```markdown
## 📋 Descrição
[Descrição da mudança]

## 🧪 Testes
- [ ] Testes unitários adicionados
- [ ] Testes de integração atualizados
- [ ] Todos os testes passando

## 📚 Documentação
- [ ] README atualizado
- [ ] Docstrings adicionadas
- [ ] Exemplos atualizados

## ✅ Checklist
- [ ] Código segue padrões PEP 8
- [ ] Type hints adicionados
- [ ] Conformidade A-SDLC verificada
- [ ] Story A-SDLC criada e documentada

## 🔗 Issue Relacionada
Closes #[número da issue]
```

### 4. Review Process

- **Code review** será realizado
- **Testes** devem passar
- **Documentação** deve estar atualizada
- **Conformidade A-SDLC** verificada

## 🏆 Reconhecimento

Contribuições significativas serão reconhecidas:

- **Mencionadas** no README
- **Badges** de contribuidor
- **Agradecimentos** em releases

## 📞 Suporte

Para dúvidas sobre contribuições:

- **Issues** - Para bugs e features
- **Discussions** - Para perguntas gerais
- **Documentação** - Para guias detalhados

---

**💡 Lembre-se: Cada contribuição ajuda a tornar o A-SDLC Framework ainda melhor!** 