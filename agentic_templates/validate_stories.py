#!/usr/bin/env python3
"""
A-SDLC Story Validator

Script simples para validar Stories antes da execucao.

Uso:

  python validate_stories.py

  python validate_stories.py stories/20260407_notificacao_push.md
"""

import sys
import re
from pathlib import Path


def parse_frontmatter(content):
    """Extrai frontmatter YAML do arquivo de forma segura."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    yaml_block = parts[1].strip()

    # Tenta usar o parser real do PyYAML se disponível
    try:
        import yaml
        data = yaml.safe_load(yaml_block)
        if isinstance(data, dict):
            normalized = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalized[k] = str(v).replace("'", '"')
                else:
                    normalized[k] = str(v)
            return normalized
    except Exception:
        pass

    # Parser manual resiliente (suporta block lists simples e flow lists)
    fm = {}
    lines = yaml_block.split("\n")
    current_key = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Se for um item de lista em bloco (ex: - "value")
        if stripped.startswith("-") and current_key:
            val_item = stripped[1:].strip().strip('"').strip("'")
            if val_item:
                existing = fm.get(current_key, "[]")
                if existing == "[]":
                    fm[current_key] = f'["{val_item}"]'
                else:
                    inner = existing.strip("[]")
                    fm[current_key] = f'[{inner}, "{val_item}"]'
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            current_key = key
            
            if val.startswith("[") and val.endswith("]"):
                fm[key] = val
            elif val == "" or val is None:
                fm[key] = "[]"
            else:
                fm[key] = val
                
    return fm


def validate_story(filepath):
    """Valida uma story."""
    content = filepath.read_text(encoding="utf-8")
    errors = []

    # Parse frontmatter
    fm = parse_frontmatter(content)
    if not fm:
        errors.append("Frontmatter nao encontrado")
        return errors

    # Valida campos obrigatorios
    required = ["title", "ticket", "status"]
    for field in required:
        if field not in fm:
            errors.append(f"Campo obrigatorio ausente: {field}")

    # Valida status
    allowed_statuses = ["PENDENTE", "CONCLUÍDO", "In Progress", "Done", "Failed", "Todo", "planned"]
    if fm.get("status") not in allowed_statuses:
        errors.append(f"Status invalido: {fm.get('status')}. Status permitidos: {allowed_statuses}")

    # Valida ticket pattern
    ticket = fm.get("ticket", "")
    if not re.match(r"^\d{8}_\w+$", ticket):
        errors.append(f"Ticket mal formatado: {ticket}")

    # Valida depends_on
    depends = fm.get("depends_on", "[]")
    if depends != "[]":
        deps = re.findall(r'"([^"]+)"', depends)
        stories_dir = filepath.parent
        for dep in deps:
            # Busca story com esse ticket
            found = False
            dep_file = None
            for f in stories_dir.glob("*.md"):
                if f.resolve() != filepath.resolve() and dep in f.read_text(encoding="utf-8"):
                    found = True
                    dep_file = f
                    break
            if not found:
                errors.append(f"Dependencia referenciada nao encontrada: {dep}")
            else:
                dep_content = dep_file.read_text(encoding="utf-8")
                dep_fm = parse_frontmatter(dep_content)
                if dep_fm:
                    dep_status = dep_fm.get("status")
                    if dep_status not in ["CONCLUÍDO", "Done"]:
                        errors.append(f"Dependencia '{dep}' ({dep_file.name}) esta no status '{dep_status}' mas deveria estar CONCLUÍDO ou Done")

    # Valida presence of test tasks (OBRIGATORIO para todas stories)
    has_test_section = "Critérios de Aceitação" in content or "Criteria" in content or "Aceitação" in content
    has_test_tasks = re.search(r"(test[e]?s?|spec|teste|pytest|cargo test|go test|npm test)", content, re.IGNORECASE)
    has_test_files = re.search(r"(\.test\.|spec\.|\.spec\.|/tests/)", content)
    has_test_commands = re.search(r"(execute|rode|roda|run command|cmd)", content, re.IGNORECASE)

    if not (has_test_section or has_test_tasks or has_test_files or has_test_commands):
        errors.append("Story deve incluir secao 'Criterios de Aceitação' com criterio testavel")

    return errors


def main():
    stories_dir = Path("stories")

    if len(sys.argv) > 1:
        files = [Path(sys.argv[1])]
    else:
        if stories_dir.exists():
            files = sorted(stories_dir.rglob("*.md"))
        else:
            files = []

    # Exclusao explicita para o arquivo MEMORY.md, pastas de templates e arquivos de template
    files = [f for f in files if f.name != "MEMORY.md" and "templates" not in f.parts and not f.name.endswith("template.md")]

    all_valid = True
    for f in files:
        errors = validate_story(f)
        if errors:
            print(f"X {f.name}")
            for e in errors:
                print(f"  - {e}")
            all_valid = False
        else:
            print(f"OK {f.name}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
