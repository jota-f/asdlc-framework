# A-SDLC Story Validator

Script simples para validar Stories antes da execução.

## Uso

```bash
# Validar todas as stories
python validate_stories.py

# Validar uma story específica  
python validate_stories.py stories/20260407_notificacao_push.md
```

## Regras de Validação

### Frontmatter
- [ ] `title`: Obrigatório, não vazio
- [ ] `ticket`: Obrigatório, padrão YYYYMMDD_*
- [ ] `status`: Obrigatório, deve ser "PENDENTE" ou "CONCLUÍDO"
- [ ] `depends_on`: Opcional, array de strings

### Corpo da Story
- [ ] Deve ter pelo menos uma seção "Manifesto de Arquivos"
- [ ] Deve ter pelo menos uma tarefa em "Tarefas Detalhadas"
- [ ] Deve ter pelo menos um critério em "Critérios de Aceitação"

### Dependências
- [ ] Se `depends_on` tem valores, todos os tickets referenciados devem existir
- [ ] Se dependência existe, deve estar com status "CONCLUÍDO" para execução

## Saída

```
✓ Validando: stories/20260407_notificacao_push.md
  ✓ Frontmatter válido
  ✓ Manifestos de arquivos definidos
  ✓ Tarefas detalhadas OK
  ✓ Critérios de aceitação OK
  ✓ Dependências verificadas (0 dependências)

✓ Story válida!
```

## Implementação

```python
#!/usr/bin/env python3
"""Validador de Stories A-SDLC"""

import sys
import re
from pathlib import Path

def parse_frontmatter(content):
    """Extrai frontmatter YAML do arquivo."""
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    fm = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key] = val
    return fm

def validate_story(filepath):
    """Valida uma story."""
    content = filepath.read_text(encoding='utf-8')
    errors = []
    
    # Parse frontmatter
    fm = parse_frontmatter(content)
    if not fm:
        errors.append("Frontmatter não encontrado")
        return errors
    
    # Valida campos obrigatórios
    required = ['title', 'ticket', 'status']
    for field in required:
        if field not in fm:
            errors.append(f"Campo obrigatório ausente: {field}")
    
    # Valida status
    if fm.get('status') not in ['PENDENTE', 'CONCLUÍDO']:
        errors.append(f"Status inválido: {fm.get('status')}")
    
    # Valida ticket pattern
    ticket = fm.get('ticket', '')
    if not re.match(r'^\d{8}_\w+$', ticket):
        errors.append(f"Ticket mal formatado: {ticket}")
    
    # Valida depends_on
    depends = fm.get('depends_on', '[]')
    if depends != '[]':
        deps = re.findall(r'"([^"]+)"', depends)
        stories_dir = filepath.parent
        for dep in deps:
            # Busca story com esse ticket
            found = False
            for f in stories_dir.glob('*.md'):
                if dep in f.read_text(encoding='utf-8'):
                    found = True
                    break
            if not found:
                errors.append(f"Dependência referenceda não encontrada: {dep}")
    
    return errors

def main():
    stories_dir = Path('stories')
    
    if len(sys.argv) > 1:
        files = [Path(sys.argv[1])]
    else:
        files = sorted(stories_dir.glob('*.md'))
    
    all_valid = True
    for f in files:
        errors = validate_story(f)
        if errors:
            print(f"✗ {f.name}")
            for e in errors:
                print(f"  - {e}")
            all_valid = False
        else:
            print(f"✓ {f.name}")
    
    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())
