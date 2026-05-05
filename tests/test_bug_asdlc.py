"""
Testes de verificação para funcionalidade de Bugs e Regressões no A-SDLC
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Importar módulos do framework
from asdlc.story_manager import create_story
from asdlc.plan_generator import gerar_plano_de_execucao
from asdlc.project_manager import initialize_project


class TestBugASDLC:
    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("asdlc.plan_generator.call_llm")
    def test_bug_story_creation(self, mock_llm):
        """Testa se a criação de uma story do tipo bug funciona e gera o plano correto"""
        # Configurar mock da LLM para retornar um plano simulado
        mock_llm.return_value = (
            '---\ntitle: "Bug Test"\nticket: "TEST_ID"\nstatus: "PENDENTE"\ntype: "bug_fix"\n---\n# Plano de Teste de Bug'
        )

        # Inicializar um projeto fake
        initialize_project("test_proj", "Test prompt", "web_api")
        os.chdir(self.temp_dir / "test_proj")

        # Criar uma story de bug
        story_id = create_story(
            story_title="Erro no Login", story_description="Falha ao logar com email XPTO", story_type="bug_fix"
        )

        assert story_id is not None

        # Verificar se o arquivo foi criado
        stories_dir = Path("stories")
        story_files = list(stories_dir.glob("*.md"))
        assert len(story_files) >= 2  # 1 do init + 1 do nosso teste

        # Encontrar o arquivo da nossa story
        bug_story_file = next(f for f in story_files if "erro_no_login" in f.name)
        content = bug_story_file.read_text(encoding="utf-8")

        # Verificar se o frontmatter contém o tipo correto
        assert 'type: "bug_fix"' in content

    @patch("asdlc.plan_generator.call_llm")
    def test_bug_hunter_agent_exists_in_new_projects(self, mock_llm):
        """Verifica se o novo agente Bug Hunter é criado na inicialização de projetos"""
        mock_llm.return_value = "# Plano de teste"
        initialize_project("test_agents", "Test prompt", "web_api")

        bug_hunter_path = self.temp_dir / "test_agents" / ".asdlc" / "agents" / "bug_hunter_agent.md"
        assert bug_hunter_path.exists()

        content = bug_hunter_path.read_text(encoding="utf-8")
        assert "Bug Hunter Agent" in content
        assert "RCA" in content


if __name__ == "__main__":
    pytest.main([__file__])
