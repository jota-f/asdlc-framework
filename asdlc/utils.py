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
    for path in sorted(project_root.rglob('*')):
        # Ignora diretórios comuns para manter a saída limpa
        if '.git' in path.parts or '__pycache__' in path.parts or 'venv' in path.parts:
            continue
        
        # Calcula a profundidade para a indentação
        depth = len(path.relative_to(project_root).parts) - 1
        indent = '    ' * depth
        
        # Adiciona um marcador se for um diretório
        marker = '📁' if path.is_dir() else '📄'
        
        structure.append(f"{indent}└── {marker} {path.name}")
    return "\n".join(structure) 