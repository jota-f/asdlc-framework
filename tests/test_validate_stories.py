import sys
import tempfile
import shutil
from pathlib import Path
import pytest

# Adicionar a pasta agentic_templates ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / "agentic_templates"))

from validate_stories import parse_frontmatter, validate_story


class TestValidateStories:
    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_frontmatter_yaml(self):
        content = """---
title: "Test Story"
status: "PENDENTE"
depends_on: ["20260614_dep"]
---
# Description
"""
        fm = parse_frontmatter(content)
        assert fm is not None
        assert fm.get("title") == "Test Story"
        assert fm.get("status") == "PENDENTE"
        assert "20260614_dep" in fm.get("depends_on")

    def test_validate_story_no_dependencies(self):
        story_file = self.temp_dir / "20260614_story.md"
        story_file.write_text(
            """---
title: "My Story"
ticket: "20260614_story"
status: "PENDENTE"
depends_on: []
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar com pytest.
""",
            encoding="utf-8",
        )

        errors = validate_story(story_file)
        assert len(errors) == 0

    def test_validate_story_dependency_not_found(self):
        story_file = self.temp_dir / "20260614_story.md"
        story_file.write_text(
            """---
title: "My Story"
ticket: "20260614_story"
status: "PENDENTE"
depends_on: ["20260614_missing_dep"]
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar com pytest.
""",
            encoding="utf-8",
        )

        errors = validate_story(story_file)
        assert len(errors) > 0
        assert any("Dependencia referenciada nao encontrada" in e for e in errors)

    def test_validate_story_dependency_pending(self):
        # Criar a dependência como PENDENTE
        dep_file = self.temp_dir / "20260614_dep.md"
        dep_file.write_text(
            """---
title: "Dependency Story"
ticket: "20260614_dep"
status: "PENDENTE"
depends_on: []
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar.
""",
            encoding="utf-8",
        )

        # Criar a story que depende da anterior
        story_file = self.temp_dir / "20260614_story.md"
        story_file.write_text(
            """---
title: "My Story"
ticket: "20260614_story"
status: "PENDENTE"
depends_on: ["20260614_dep"]
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar com pytest.
""",
            encoding="utf-8",
        )

        errors = validate_story(story_file)
        assert len(errors) > 0
        assert any("deveria estar CONCLUÍDO ou Done" in e for e in errors)

    def test_validate_story_dependency_done(self):
        # Criar a dependência como CONCLUÍDO
        dep_file = self.temp_dir / "20260614_dep.md"
        dep_file.write_text(
            """---
title: "Dependency Story"
ticket: "20260614_dep"
status: "CONCLUÍDO"
depends_on: []
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar.
""",
            encoding="utf-8",
        )

        # Criar a story que depende da anterior
        story_file = self.temp_dir / "20260614_story.md"
        story_file.write_text(
            """---
title: "My Story"
ticket: "20260614_story"
status: "PENDENTE"
depends_on: ["20260614_dep"]
---
# Plano de Execução
## ✅ Critérios de Aceitação
- Testar com pytest.
""",
            encoding="utf-8",
        )

        errors = validate_story(story_file)
        assert len(errors) == 0
