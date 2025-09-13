"""
Testes básicos para o A-SDLC Framework
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Importar módulos do framework
from asdlc.project_manager import ProjectManager
from asdlc.story_manager import StoryManager
from asdlc.plan_generator import PlanGenerator
from asdlc.ui_manager import UIManager


class TestProjectManager:
    """Testes para o ProjectManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_manager = ProjectManager()
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_project_structure(self):
        """Testa criação de estrutura de projeto"""
        project_name = "test-project"
        project_type = "cli"
        
        # Mock para evitar chamadas reais de API
        with patch('asdlc.project_manager.PlanGenerator') as mock_plan_gen:
            mock_plan_gen.return_value.generate_project_context.return_value = "Contexto de teste"
            
            result = self.project_manager.create_project_structure(
                project_name, project_type, self.temp_dir
            )
            
            assert result is True
            project_path = os.path.join(self.temp_dir, project_name)
            assert os.path.exists(project_path)
            assert os.path.exists(os.path.join(project_path, "PROJECT_CONTEXT.md"))
            assert os.path.exists(os.path.join(project_path, ".asdlc"))
            assert os.path.exists(os.path.join(project_path, "stories"))
            assert os.path.exists(os.path.join(project_path, "prompts"))
    
    def test_validate_project_type(self):
        """Testa validação de tipos de projeto"""
        valid_types = ["web_frontend", "web_api", "cli", "mobile", "desktop"]
        
        for project_type in valid_types:
            assert self.project_manager.validate_project_type(project_type) is True
        
        assert self.project_manager.validate_project_type("invalid_type") is False


class TestStoryManager:
    """Testes para o StoryManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.story_manager = StoryManager()
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_story(self):
        """Testa criação de story"""
        story_title = "Test Story"
        story_description = "Uma story de teste"
        project_type = "cli"
        
        # Mock para evitar chamadas reais de API
        with patch('asdlc.story_manager.PlanGenerator') as mock_plan_gen:
            mock_plan_gen.return_value.generate_plan.return_value = "Plano de teste"
            
            result = self.story_manager.create_story(
                story_title, story_description, project_type, self.temp_dir
            )
            
            assert result is True
            stories_dir = os.path.join(self.temp_dir, "stories")
            assert os.path.exists(stories_dir)
            
            # Verificar se o arquivo da story foi criado
            story_files = [f for f in os.listdir(stories_dir) if f.endswith('.md')]
            assert len(story_files) > 0


class TestPlanGenerator:
    """Testes para o PlanGenerator"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.plan_generator = PlanGenerator()
    
    def test_generate_project_context(self):
        """Testa geração de contexto de projeto"""
        project_name = "test-project"
        project_type = "cli"
        prompt = "API de gestão de usuários"
        
        # Mock para evitar chamadas reais de API
        with patch('asdlc.plan_generator.LLMClient') as mock_llm:
            mock_llm.return_value.generate_response.return_value = "Contexto gerado"
            
            result = self.plan_generator.generate_project_context(
                project_name, project_type, prompt
            )
            
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_generate_plan(self):
        """Testa geração de plano"""
        story_title = "Test Story"
        story_description = "Uma story de teste"
        project_type = "cli"
        
        # Mock para evitar chamadas reais de API
        with patch('asdlc.plan_generator.LLMClient') as mock_llm:
            mock_llm.return_value.generate_response.return_value = "Plano gerado"
            
            result = self.plan_generator.generate_plan(
                story_title, story_description, project_type
            )
            
            assert isinstance(result, str)
            assert len(result) > 0


class TestUIManager:
    """Testes para o UIManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.ui_manager = UIManager()
    
    def test_display_menu(self):
        """Testa exibição do menu"""
        # Mock para input/output
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mock_print:
                result = self.ui_manager.display_menu()
                
                assert mock_print.called
                assert result == '1'
    
    def test_get_project_info(self):
        """Testa obtenção de informações do projeto"""
        # Mock para input
        with patch('builtins.input', side_effect=['test-project', 'API de teste', 'cli']):
            result = self.ui_manager.get_project_info()
            
            assert isinstance(result, dict)
            assert 'project_name' in result
            assert 'prompt' in result
            assert 'project_type' in result
            assert result['project_name'] == 'test-project'
            assert result['prompt'] == 'API de teste'
            assert result['project_type'] == 'cli'


class TestFrameworkIntegration:
    """Testes de integração do framework"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """Testa workflow completo do framework"""
        # Mock para todas as chamadas de API
        with patch('asdlc.plan_generator.LLMClient') as mock_llm:
            mock_llm.return_value.generate_response.return_value = "Resposta de teste"
            
            # Criar projeto
            project_manager = ProjectManager()
            result = project_manager.create_project_structure(
                "test-project", "cli", self.temp_dir
            )
            assert result is True
            
            # Criar story
            story_manager = StoryManager()
            result = story_manager.create_story(
                "Test Story", "Uma story de teste", "cli", 
                os.path.join(self.temp_dir, "test-project")
            )
            assert result is True
            
            # Verificar estrutura final
            project_path = os.path.join(self.temp_dir, "test-project")
            assert os.path.exists(project_path)
            assert os.path.exists(os.path.join(project_path, "stories"))
            assert os.path.exists(os.path.join(project_path, "prompts"))
            assert os.path.exists(os.path.join(project_path, "PROJECT_CONTEXT.md"))


if __name__ == "__main__":
    pytest.main([__file__]) 