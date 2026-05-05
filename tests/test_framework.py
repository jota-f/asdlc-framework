"""
Testes básicos para o A-SDLC Framework
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Importar módulos do framework (API funcional)
from asdlc.project_manager import initialize_project
from asdlc.story_manager import create_story, list_stories
from asdlc.plan_generator import gerar_plano_de_execucao
from asdlc.ui_manager import UIManager


class TestInitializeProject:
    """Testes para initialize_project"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("asdlc.project_manager.story_manager.create_story")
    def test_initialize_project_creates_structure(self, mock_create_story):
        """Testa criação de estrutura de projeto"""
        project_name = "test-project"
        initial_prompt = "CLI para gerenciar tarefas"
        project_type = "cli"

        project_dir = Path(self.temp_dir) / project_name
        initialize_project(project_name, initial_prompt, project_type, project_path=str(project_dir))

        assert project_dir.exists()
        assert (project_dir / "PROJECT_CONTEXT.md").exists()
        assert (project_dir / ".asdlc").exists()
        assert (project_dir / ".asdlc" / "agents").exists()
        assert (project_dir / "stories").exists()
        assert (project_dir / "prompts").exists()

    @patch("asdlc.project_manager.story_manager.create_story")
    def test_initialize_project_creates_agent_templates(self, mock_create_story):
        """Testa criação de templates de agentes"""
        project_name = "test-agents"
        project_dir = Path(self.temp_dir) / project_name
        initialize_project(project_name, "teste", "cli", project_path=str(project_dir))

        agents_dir = project_dir / ".asdlc" / "agents"
        expected_agents = [
            "code_agent.md",
            "test_agent.md",
            "architecture_agent.md",
            "requirements_agent.md",
            "review_agent.md",
            "bug_hunter_agent.md",
        ]
        for agent_file in expected_agents:
            assert (agents_dir / agent_file).exists(), f"Agent file {agent_file} not found"

    @patch("asdlc.project_manager.story_manager.create_story")
    def test_initialize_project_creates_prompt_templates(self, mock_create_story):
        """Testa criação de templates de prompts"""
        project_name = "test-prompts"
        project_dir = Path(self.temp_dir) / project_name
        initialize_project(project_name, "teste", "cli", project_path=str(project_dir))

        prompts_dir = project_dir / "prompts"
        assert prompts_dir.exists()
        assert (prompts_dir / "project_description_generator.md").exists()
        assert (prompts_dir / "story_generator.md").exists()

    @patch("asdlc.project_manager.story_manager.create_story")
    def test_initialize_project_creates_project_context(self, mock_create_story):
        """Testa criação do PROJECT_CONTEXT.md"""
        project_name = "test-context"
        project_dir = Path(self.temp_dir) / project_name
        initialize_project(project_name, "Minha descrição", "web_api", project_path=str(project_dir))

        context_file = project_dir / "PROJECT_CONTEXT.md"
        content = context_file.read_text(encoding="utf-8")
        assert project_name in content
        assert "Minha descrição" in content


class TestCreateStory:
    """Testes para create_story"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir) / "test-project"
        self.project_dir.mkdir()
        (self.project_dir / ".asdlc").mkdir()
        (self.project_dir / "stories").mkdir()

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("asdlc.story_manager.gerar_plano_de_execucao")
    @patch("asdlc.story_manager.find_project_root")
    def test_create_story_returns_id(self, mock_find_root, mock_gen_plan):
        """Testa que create_story retorna um ID"""
        mock_find_root.return_value = self.project_dir
        mock_gen_plan.return_value = "# Plano de teste"

        story_id = create_story(story_title="Teste de Login", story_description="Implementar login")

        assert story_id is not None
        assert isinstance(story_id, str)

    @patch("asdlc.story_manager.gerar_plano_de_execucao")
    @patch("asdlc.story_manager.find_project_root")
    def test_create_story_creates_file(self, mock_find_root, mock_gen_plan):
        """Testa que create_story cria um arquivo .md"""
        mock_find_root.return_value = self.project_dir
        mock_gen_plan.return_value = "# Plano de teste"

        create_story(story_title="Teste de API", story_description="Criar endpoint")

        stories_dir = self.project_dir / "stories"
        story_files = list(stories_dir.glob("*.md"))
        assert len(story_files) > 0


class TestListStories:
    """Testes para list_stories"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir) / "test-project"
        self.project_dir.mkdir()
        (self.project_dir / ".asdlc").mkdir()
        (self.project_dir / "stories").mkdir()

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("asdlc.story_manager.find_project_root")
    def test_list_stories_empty(self, mock_find_root):
        """Testa list_stories quando não há stories"""
        mock_find_root.return_value = self.project_dir
        stories = list_stories()
        assert stories == []

    @patch("asdlc.story_manager.find_project_root")
    def test_list_stories_with_files(self, mock_find_root):
        """Testa list_stories com stories existentes"""
        mock_find_root.return_value = self.project_dir

        # Criar uma story manualmente
        story_content = """---
title: "Test Story"
ticket: "20260504_test_story"
status: "PENDENTE"
priority: "P1"
labels: []
depends_on: []
---

# Plano de Execução: Test Story

## Teste
"""
        story_file = self.project_dir / "stories" / "20260504_test_story.md"
        story_file.write_text(story_content, encoding="utf-8")

        stories = list_stories()
        assert len(stories) == 1
        assert stories[0].get("title") == "Test Story"


class TestGerarPlanoDeExecucao:
    """Testes para gerar_plano_de_execucao"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir)
        # Criar PROJECT_CONTEXT.md mínimo
        (self.project_dir / "PROJECT_CONTEXT.md").write_text("# Contexto de teste", encoding="utf-8")

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("asdlc.plan_generator.call_llm")
    def test_gerar_plano_returns_string(self, mock_call_llm):
        """Testa que gerar_plano_de_execucao retorna uma string"""
        mock_call_llm.return_value = "# Plano gerado"

        story_data = {
            "title": "Teste",
            "id": "20260504_teste",
            "description": "Descrição de teste",
            "type": "user_story",
        }

        result = gerar_plano_de_execucao(story_data, self.project_dir)

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("asdlc.plan_generator.call_llm")
    def test_gerar_plano_calls_llm(self, mock_call_llm):
        """Testa que gerar_plano_de_execucao chama a LLM"""
        mock_call_llm.return_value = "# Plano"

        story_data = {
            "title": "Teste",
            "id": "20260504_teste",
            "description": "Descrição",
            "type": "user_story",
        }

        gerar_plano_de_execucao(story_data, self.project_dir)

        mock_call_llm.assert_called_once()


class TestUIManager:
    """Testes para UIManager"""

    def test_ui_manager_has_methods(self):
        """Testa que UIManager tem os métodos esperados"""
        ui = UIManager()
        assert hasattr(ui, "show_banner")
        assert hasattr(ui, "show_menu")
        assert hasattr(ui, "execute_menu_choice")
        assert hasattr(ui, "start_interactive_mode")


class TestAgentExecutor:
    """Testes para agent_executor"""

    def test_estimate_token_count(self):
        """Testa estimativa de tokens"""
        from asdlc.agent_executor import estimate_token_count

        # 4 caracteres ≈ 1 token
        assert estimate_token_count("1234") == 1
        assert estimate_token_count("12345678") == 2
        assert estimate_token_count("") == 0

    def test_log_context_density_ok(self):
        """Testa log de contexto na Smart Zone"""
        from asdlc.agent_executor import log_context_density

        # 10k chars ≈ 2.5k tokens - deve estar na Smart Zone
        tokens = log_context_density("test", 10000)
        assert tokens == 2500

    def test_log_context_density_warning(self):
        """Testa log de contexto na Warning Zone"""
        from asdlc.agent_executor import log_context_density

        # 400k chars ≈ 100k tokens - deve estar na Warning/Dumb Zone
        tokens = log_context_density("test", 400000)
        assert tokens == 100000


if __name__ == "__main__":
    pytest.main([__file__])
