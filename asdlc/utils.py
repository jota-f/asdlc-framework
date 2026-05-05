import logging
import os
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Instância central do Console
console = Console(force_terminal=True, color_system="auto", width=100)


def is_headless() -> bool:
    """Detecta se o terminal é interativo."""
    return not sys.stdout.isatty() or os.getenv("TERM") == "dumb"


def find_project_root() -> Optional[Path]:
    """Encontra a raiz do projeto A-SDLC."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".asdlc").exists() or (parent / "PROJECT_CONTEXT.md").exists() or (parent / "asdlc").exists():
            return parent
    return None


def get_project_structure(project_root: Path) -> str:
    """Gera uma representação em string da estrutura de arquivos do projeto."""
    structure = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "venv", ".venv", ".gemini", "node_modules"]]
        level = Path(root).relative_to(project_root).parts
        indent = "  " * len(level)
        structure.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = "  " * (len(level) + 1)
        for f in files:
            structure.append(f"{sub_indent}{f}")
    return "\n".join(structure)


def safe_write_file(path: Path, content: str):
    """Escreve um arquivo de forma segura."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    print(f"--- [ARQUIVO CRIADO]: {path.absolute()} ---")


def detect_test_framework(project_root: Path) -> str:
    """Detecta qual framework de teste está sendo usado."""
    if (project_root / "pytest.ini").exists() or (project_root / "tests").exists():
        return "pytest"
    if (project_root / "jest.config.js").exists() or (project_root / "package.json").exists():
        return "jest"
    return "unittest"
