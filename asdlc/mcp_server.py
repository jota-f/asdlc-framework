"""
A-SDLC MCP Server
Expondo as ferramentas do framework A-SDLC via Model Context Protocol.

FERRAMENTAS DE GESTÃO (funcionam sempre):
  - asdlc_create_project, asdlc_create_story, asdlc_validate_project
  - asdlc_get_story_details, asdlc_update_story_status
  - asdlc_get_project_metrics, asdlc_list_stories

FERRAMENTAS DE EXECUÇÃO (requerem ASDLC_ENGINE=external no .env):
  - asdlc_implement_story, asdlc_spawn_specialist
"""

from fastmcp import FastMCP
from pathlib import Path
import os
import logging
from typing import Optional

# Importar lógica interna do A-SDLC
from asdlc import project_manager, story_manager, utils
from asdlc.validation_checker import ASDLCValidator

# Configurar logging para o servidor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("asdlc-mcp")

# Criar o servidor MCP
mcp = FastMCP("A-SDLC Framework")

# ============================================
# FERRAMENTAS DE GESTÃO (sempre disponíveis)
# ============================================


@mcp.tool()
def asdlc_create_project(name: str, prompt: str, path: Optional[str] = None, type: str = "web_api") -> str:
    """
    Cria ou inicializa um novo projeto A-SDLC.

    Args:
        name: Nome do projeto
        prompt: Objetivo principal do projeto
        path: Caminho opcional para a pasta do projeto (se vazio, usa o diretório atual)
        type: Tipo do projeto (web_api, embedded, mobile, etc)
    """
    try:
        project_manager.initialize_project(project_name=name, initial_prompt=prompt, project_type=type, project_path=path)
        return f"Projeto '{name}' inicializado com sucesso em {path or os.getcwd()}."
    except Exception as e:
        return f"Erro ao criar projeto: {str(e)}"


@mcp.tool()
def asdlc_create_story(title: str, description: Optional[str] = None) -> str:
    """
    Cria uma nova story com plano de execução no projeto ativo.
    """
    try:
        story_id = story_manager.create_story(story_title=title, story_description=description)
        if story_id:
            return f"Story '{title}' criada com sucesso! ID: {story_id}"
        return "Erro: Não foi possível criar a story. Verifique se você está em um projeto A-SDLC."
    except Exception as e:
        return f"Erro ao criar story: {str(e)}"


@mcp.tool()
def asdlc_validate_project(project_path: str = ".") -> str:
    """
    Valida se o projeto segue os padrões e leis do A-SDLC.
    """
    try:
        validator = ASDLCValidator(Path(project_path))
        report = validator.validate_project()
        formatted = validator.generate_report("text")
        return formatted
    except Exception as e:
        return f"Erro ao validar projeto: {str(e)}"


@mcp.tool()
def asdlc_get_story_details(story_id: str) -> str:
    """
    Retorna o conteúdo completo de uma story para análise.
    """
    try:
        story_path = story_manager._encontrar_story_por_id(story_id)
        if story_path:
            return story_path.read_text(encoding="utf-8")
        return f"Erro: Story {story_id} não encontrada."
    except Exception as e:
        return f"Erro ao ler story: {str(e)}"


@mcp.tool()
def asdlc_update_story_status(story_id: str, status: str) -> str:
    """
    Atualiza o status de uma story (ex: Todo, In Progress, Done, Review, Failed).
    """
    try:
        story_path = story_manager._encontrar_story_por_id(story_id)
        if story_path:
            story_manager._atualizar_status_story(story_path, status)
            return f"Status da story {story_id} atualizado para '{status}'."
        return f"Erro: Story {story_id} não encontrada."
    except Exception as e:
        return f"Erro ao atualizar status: {str(e)}"


@mcp.tool()
def asdlc_get_project_metrics() -> str:
    """
    Retorna métricas de progresso de todo o projeto.
    """
    try:
        project_root = utils.find_project_root()
        if not project_root:
            return "Erro: Projeto não encontrado."

        stories_dir = project_root / "stories"
        if not stories_dir.exists():
            return "Sem métricas: Nenhuma story encontrada."

        all_metrics = []
        for f in stories_dir.glob("*.md"):
            m = story_manager._calcular_metricas_story(f)
            story_id = f.stem.split("_")[0]
            all_metrics.append(f"Story {story_id}: {m.get('progress_percentage', 0)}% concluída")

        return "Métricas do Projeto:\n" + "\n".join(all_metrics)
    except Exception as e:
        return f"Erro ao calcular métricas: {str(e)}"


@mcp.tool()
def asdlc_list_stories() -> str:
    """
    Lista todas as stories e seus status no projeto atual.
    """
    try:
        project_root = utils.find_project_root()
        if not project_root:
            return "Erro: Nenhum projeto A-SDLC encontrado."

        stories_dir = project_root / "stories"
        if not stories_dir.exists():
            return "Nenhuma story encontrada (pasta /stories vazia)."

        stories = []
        for f in stories_dir.glob("*.md"):
            stories.append(f"- {f.name}")

        return "Stories encontradas:\n" + "\n".join(stories)
    except Exception as e:
        return f"Erro ao listar stories: {str(e)}"


# ============================================
# FERRAMENTAS DE EXECUÇÃO (requerem ASDLC_ENGINE=external)
# ============================================


@mcp.tool()
def asdlc_implement_story(story_id: str, project_path: Optional[str] = None) -> str:
    """
    [REQUER ASDLC_ENGINE=external] Inicia a implementação automatizada de uma story
    usando o motor Python com API externa. Se ASDLC_ENGINE=antigravity, retorna
    instrução para usar a Skill no chat.

    Args:
        story_id: O ID da story (timestamp no início do nome do arquivo)
        project_path: Caminho opcional para a pasta do projeto
    """
    from dotenv import load_dotenv

    load_dotenv()
    engine = os.getenv("ASDLC_ENGINE", "antigravity").lower()

    if engine != "external":
        return (
            f"MODO ANTIGRAVITY ATIVO: Esta ferramenta requer ASDLC_ENGINE=external no .env.\n"
            f"Para implementar a story {story_id} usando o Antigravity (sem custo de API):\n"
            f"1. Use a Skill @asdlc_implementation no chat\n"
            f"2. Leia a story com asdlc_get_story_details('{story_id}')\n"
            f"3. Execute os passos manualmente usando view_file, write_file e run_command\n"
            f"4. Atualize o status com asdlc_update_story_status('{story_id}', 'Done')"
        )

    try:
        if project_path:
            os.chdir(project_path)
        success = story_manager.implement_story(story_id=story_id)
        if success:
            return f"Implementação da story {story_id} concluída com sucesso."
        return f"Falha na implementação da story {story_id}."
    except Exception as e:
        return f"Erro durante a implementação: {str(e)}"


@mcp.tool()
def asdlc_spawn_specialist(agent_type: str, task: str, files: Optional[str] = None, project_path: Optional[str] = None) -> str:
    """
    [REQUER ASDLC_ENGINE=external] Invoca um agente especialista isolado para uma
    tarefa específica usando o motor Python com API externa.

    Args:
        agent_type: code, test, architecture, requirements, review, bug_hunter
        task: Descrição da tarefa
        files: Lista de arquivos separados por vírgula (opcional)
        project_path: Caminho opcional para a pasta do projeto
    """
    from dotenv import load_dotenv

    load_dotenv()
    engine = os.getenv("ASDLC_ENGINE", "antigravity").lower()

    if engine != "external":
        return (
            f"MODO ANTIGRAVITY ATIVO: Esta ferramenta requer ASDLC_ENGINE=external no .env.\n"
            f"No modo Antigravity, a IDE assume o papel de '{agent_type}' diretamente.\n"
            f"Use a Skill @asdlc_implementation e peça a tarefa no chat."
        )

    try:
        if project_path:
            os.chdir(project_path)
        relevant_files = [f.strip() for f in files.split(",")] if files else []
        result = story_manager.spawn_agent(agent_type, "adhoc_task", task, relevant_files)
        return result
    except Exception as e:
        return f"Erro ao invocar especialista: {str(e)}"


if __name__ == "__main__":
    mcp.run()
