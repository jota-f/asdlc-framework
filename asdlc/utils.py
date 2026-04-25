# asdlc/utils.py
"""
Módulo de utilitários para o framework A-SDLC.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def find_project_root() -> Optional[Path]:
    """Encontra a raiz do projeto A-SDLC."""
    current = Path.cwd()

    # Procura por indicadores de projeto A-SDLC
    while current != current.parent:
        if (current / ".asdlc").exists() or (current / "PROJECT_CONTEXT.md").exists():
            return current
        current = current.parent

    return None


def get_project_structure(project_root: Path) -> str:
    """Gera uma representação em string da estrutura de arquivos do projeto."""
    structure = []
    for path in sorted(project_root.rglob("*")):
        # Ignora diretórios comuns para manter a saída limpa
        if ".git" in path.parts or "__pycache__" in path.parts or "venv" in path.parts:
            continue

        # Calcula a profundidade para a indentação
        depth = len(path.relative_to(project_root).parts) - 1
        indent = "    " * depth

        # Adiciona um marcador se for um diretório
        marker = "📁" if path.is_dir() else "📄"

        structure.append(f"{indent}└── {marker} {path.name}")
    return "\n".join(structure)


def detect_test_framework(project_root: Path) -> Optional[str]:
    """
    Detecta o framework de testes baseado nos arquivos e contexto do projeto.
    """
    # 1. Verificar PROJECT_CONTEXT.md
    context_file = project_root / "PROJECT_CONTEXT.md"
    if context_file.exists():
        content = context_file.read_text(encoding="utf-8").lower()
        if "pytest" in content:
            return "pytest"
        if "jest" in content:
            return "jest"
        if "unittest" in content:
            return "unittest"
        if "cypress" in content:
            return "cypress"

    # 2. Verificar arquivos de configuração
    indicators = {
        "pytest.ini": "pytest",
        "conftest.py": "pytest",
        "jest.config.js": "jest",
        "package.json": "npm_test",  # Pode ser jest, mocha, etc.
        "requirements.txt": "python_test",
        "pyproject.toml": "python_test",
    }

    for file, framework in indicators.items():
        if (project_root / file).exists():
            # Se for package.json, tentar ler o script de test
            if file == "package.json":
                try:
                    import json
                    with open(project_root / file, "r") as f:
                        data = json.load(f)
                        test_script = data.get("scripts", {}).get("test", "")
                        if "jest" in test_script: return "jest"
                        if "mocha" in test_script: return "mocha"
                except:
                    pass
            
            # Se for python, verificar se pytest está no requirements
            if file in ["requirements.txt", "pyproject.toml"]:
                content = (project_root / file).read_text(encoding="utf-8").lower()
                if "pytest" in content: return "pytest"
                if "unittest" in content: return "unittest"

            return framework

    return None
