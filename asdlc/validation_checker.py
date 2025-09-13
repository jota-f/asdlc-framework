"""
A-SDLC Framework - Validador de Conformidade
Módulo responsável por validar se projetos seguem corretamente os padrões A-SDLC
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import yaml
from datetime import datetime
import re

# Configurar logging
logger = logging.getLogger(__name__)

class ASDLCValidator:
    """Validador de conformidade A-SDLC"""
    
    def __init__(self, project_path: Path):
        """
        Inicializar validador para um projeto específico
        
        Args:
            project_path: Caminho para o projeto a ser validado
        """
        self.project_path = Path(project_path)
        self.validation_report = {
            'project_name': self.project_path.name,
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0,
            'validations': {},
            'suggestions': [],
            'auto_fix_commands': []
        }
    
    def validate_project(self) -> Dict[str, Any]:
        """
        Executar validação completa do projeto A-SDLC
        
        Returns:
            Dict com relatório completo de validação
        """
        logger.info(f"🔍 Iniciando validação A-SDLC para: {self.project_path.name}")
        
        # 1. Validar estrutura de arquivos
        structure_score = self._validate_file_structure()
        
        # 2. Validar conteúdo dos agentes
        agents_score = self._validate_agent_content()
        
        # 3. Validar stories bem formadas
        stories_score = self._validate_stories_format()
        
        # 4. Validar PROJECT_CONTEXT.md
        context_score = self._validate_project_context()
        
        # 5. Validar prompts
        prompts_score = self._validate_prompts()
        
        # Calcular score geral
        self.validation_report['overall_score'] = (
            structure_score + agents_score + stories_score + 
            context_score + prompts_score
        ) / 5
        
        # Gerar sugestões de melhoria
        self._generate_improvement_suggestions()
        
        logger.info(f"✅ Validação concluída. Score: {self.validation_report['overall_score']:.1f}/100")
        
        return self.validation_report
    
    def _validate_file_structure(self) -> float:
        """Validar estrutura de arquivos obrigatória"""
        logger.info("📁 Validando estrutura de arquivos...")
        
        required_files = [
            'PROJECT_CONTEXT.md',
            '.asdlc/agents/code_agent.md',
            '.asdlc/agents/test_agent.md', 
            '.asdlc/agents/architecture_agent.md',
            '.asdlc/agents/requirements_agent.md',
            '.asdlc/agents/review_agent.md'
        ]
        
        required_dirs = [
            '.asdlc',
            '.asdlc/agents',
            'stories',
            'prompts'
        ]
        
        structure_validations = {}
        score = 0
        total_checks = len(required_files) + len(required_dirs)
        
        # Verificar arquivos obrigatórios
        for file_path in required_files:
            full_path = self.project_path / file_path
            exists = full_path.exists()
            structure_validations[f"file_{file_path}"] = {
                'status': '✅' if exists else '❌',
                'exists': exists,
                'path': str(full_path)
            }
            if exists:
                score += 1
            else:
                self.validation_report['suggestions'].append(
                    f"📁 Criar arquivo obrigatório: {file_path}"
                )
                self.validation_report['auto_fix_commands'].append(
                    f"touch '{file_path}'"
                )
        
        # Verificar diretórios obrigatórios
        for dir_path in required_dirs:
            full_path = self.project_path / dir_path
            exists = full_path.exists() and full_path.is_dir()
            structure_validations[f"dir_{dir_path}"] = {
                'status': '✅' if exists else '❌',
                'exists': exists,
                'path': str(full_path)
            }
            if exists:
                score += 1
            else:
                self.validation_report['suggestions'].append(
                    f"📁 Criar diretório obrigatório: {dir_path}"
                )
                self.validation_report['auto_fix_commands'].append(
                    f"mkdir -p '{dir_path}'"
                )
        
        self.validation_report['validations']['file_structure'] = structure_validations
        structure_score = (score / total_checks) * 100
        
        logger.info(f"📁 Estrutura: {structure_score:.1f}/100 ({score}/{total_checks} itens)")
        return structure_score
    
    def _validate_agent_content(self) -> float:
        """Validar conteúdo dos agentes A-SDLC"""
        logger.info("🤖 Validando conteúdo dos agentes...")
        
        agents = [
            'code_agent.md',
            'test_agent.md', 
            'architecture_agent.md',
            'requirements_agent.md',
            'review_agent.md'
        ]
        
        required_sections = [
            '# 🤖',  # Título do agente
            '## 📋 Visão Geral',
            '## 🎯 Responsabilidades Principais',
            'Persona',  # Menção de persona
            'Agent'     # Menção de agente
        ]
        
        agents_validations = {}
        total_score = 0
        
        for agent_file in agents:
            agent_path = self.project_path / '.asdlc' / 'agents' / agent_file
            agent_validations = {
                'exists': False,
                'has_content': False,
                'has_persona': False,
                'sections_found': [],
                'score': 0
            }
            
            if agent_path.exists():
                agent_validations['exists'] = True
                content = agent_path.read_text(encoding='utf-8', errors='ignore')
                
                if len(content.strip()) > 100:  # Conteúdo mínimo
                    agent_validations['has_content'] = True
                
                # Verificar seções obrigatórias
                for section in required_sections:
                    if section.lower() in content.lower():
                        agent_validations['sections_found'].append(section)
                
                # Verificar se menciona persona
                if 'persona' in content.lower():
                    agent_validations['has_persona'] = True
                
                # Calcular score do agente
                agent_score = (
                    (1 if agent_validations['exists'] else 0) +
                    (1 if agent_validations['has_content'] else 0) +
                    (1 if agent_validations['has_persona'] else 0) +
                    (len(agent_validations['sections_found']) / len(required_sections))
                ) / 4 * 100
                
                agent_validations['score'] = agent_score
                total_score += agent_score
            else:
                self.validation_report['suggestions'].append(
                    f"🤖 Criar arquivo do agente: .asdlc/agents/{agent_file}"
                )
            
            agents_validations[agent_file] = agent_validations
        
        self.validation_report['validations']['agents'] = agents_validations
        agents_score = total_score / len(agents)
        
        logger.info(f"🤖 Agentes: {agents_score:.1f}/100")
        return agents_score
    
    def _validate_stories_format(self) -> float:
        """Validar formato das stories"""
        logger.info("📝 Validando formato das stories...")
        
        stories_dir = self.project_path / 'stories'
        if not stories_dir.exists():
            self.validation_report['validations']['stories'] = {
                'dir_exists': False,
                'total_stories': 0,
                'valid_stories': 0,
                'score': 0
            }
            return 0
        
        story_files = list(stories_dir.glob('*.md'))
        valid_stories = 0
        story_validations = {}
        
        required_story_sections = [
            '---',  # Front matter
            'title:',
            'ticket:',
            '# Plano de Execução',
            '## 📝 Especificações da Story',
            '## Manifesto de Arquivos',
            '## ✅ Critérios de Aceitação'
        ]
        
        for story_file in story_files:
            story_validation = {
                'sections_found': [],
                'has_frontmatter': False,
                'has_agents_reference': False,
                'score': 0
            }
            
            try:
                content = story_file.read_text(encoding='utf-8', errors='ignore')
                
                # Verificar seções obrigatórias
                for section in required_story_sections:
                    if section in content:
                        story_validation['sections_found'].append(section)
                
                # Verificar front matter
                if content.startswith('---') and content.count('---') >= 2:
                    story_validation['has_frontmatter'] = True
                
                # Verificar referência aos agentes
                if '.asdlc/agents/' in content or 'agente' in content.lower():
                    story_validation['has_agents_reference'] = True
                
                # Calcular score da story
                story_score = (
                    (len(story_validation['sections_found']) / len(required_story_sections)) * 0.7 +
                    (1 if story_validation['has_frontmatter'] else 0) * 0.2 +
                    (1 if story_validation['has_agents_reference'] else 0) * 0.1
                ) * 100
                
                story_validation['score'] = story_score
                
                if story_score >= 70:  # 70% como limiar de "válida"
                    valid_stories += 1
                
            except Exception as e:
                logger.warning(f"Erro ao validar story {story_file}: {e}")
                story_validation['error'] = str(e)
            
            story_validations[story_file.name] = story_validation
        
        stories_score = (valid_stories / len(story_files) * 100) if story_files else 0
        
        self.validation_report['validations']['stories'] = {
            'dir_exists': True,
            'total_stories': len(story_files),
            'valid_stories': valid_stories,
            'score': stories_score,
            'details': story_validations
        }
        
        logger.info(f"📝 Stories: {stories_score:.1f}/100 ({valid_stories}/{len(story_files)} válidas)")
        return stories_score
    
    def _validate_project_context(self) -> float:
        """Validar PROJECT_CONTEXT.md"""
        logger.info("📋 Validando PROJECT_CONTEXT.md...")
        
        context_path = self.project_path / 'PROJECT_CONTEXT.md'
        
        if not context_path.exists():
            self.validation_report['validations']['project_context'] = {
                'exists': False,
                'score': 0
            }
            self.validation_report['suggestions'].append(
                "📋 Criar PROJECT_CONTEXT.md na raiz do projeto"
            )
            return 0
        
        required_sections = [
            '# 📜 PROJECT_CONTEXT.md',
            '## 1. Visão Geral do Projeto',
            '## 2. Arquitetura do Sistema',
            '## 3. Pilha de Tecnologia',
            '## 4. Funcionalidades Principais',
            '## 5. Padrões e Convenções',
            '## 6. Princípios Gerais',
            '## 7. Métricas de Qualidade',
            '## 8. Estrutura de Diretórios',
            '## 9. Configurações de Ambiente',
            '## 10. Próximos Passos'
        ]
        
        try:
            content = context_path.read_text(encoding='utf-8', errors='ignore')
            sections_found = []
            
            for section in required_sections:
                if section in content:
                    sections_found.append(section)
            
            context_score = (len(sections_found) / len(required_sections)) * 100
            
            self.validation_report['validations']['project_context'] = {
                'exists': True,
                'sections_found': sections_found,
                'total_sections': len(required_sections),
                'content_length': len(content),
                'score': context_score
            }
            
            if context_score < 80:
                self.validation_report['suggestions'].append(
                    f"📋 PROJECT_CONTEXT.md incompleto ({len(sections_found)}/{len(required_sections)} seções)"
                )
            
        except Exception as e:
            logger.warning(f"Erro ao validar PROJECT_CONTEXT.md: {e}")
            context_score = 0
        
        logger.info(f"📋 PROJECT_CONTEXT: {context_score:.1f}/100")
        return context_score
    
    def _validate_prompts(self) -> float:
        """Validar diretório de prompts"""
        logger.info("📚 Validando prompts...")
        
        prompts_dir = self.project_path / 'prompts'
        
        if not prompts_dir.exists():
            self.validation_report['validations']['prompts'] = {
                'dir_exists': False,
                'score': 0
            }
            return 0
        
        required_prompts = [
            'project_description_generator.md',
            'story_generator.md',
            'implementation_executor.md',
            'validation_checker.md',
            'README.md'
        ]
        
        prompts_found = 0
        prompts_validation = {}
        
        for prompt_file in required_prompts:
            prompt_path = prompts_dir / prompt_file
            exists = prompt_path.exists()
            prompts_validation[prompt_file] = {
                'exists': exists,
                'path': str(prompt_path)
            }
            if exists:
                prompts_found += 1
        
        prompts_score = (prompts_found / len(required_prompts)) * 100
        
        self.validation_report['validations']['prompts'] = {
            'dir_exists': True,
            'prompts_found': prompts_found,
            'total_prompts': len(required_prompts),
            'score': prompts_score,
            'details': prompts_validation
        }
        
        logger.info(f"📚 Prompts: {prompts_score:.1f}/100 ({prompts_found}/{len(required_prompts)} encontrados)")
        return prompts_score
    
    def _generate_improvement_suggestions(self):
        """Gerar sugestões de melhoria baseadas na validação"""
        score = self.validation_report['overall_score']
        
        if score < 50:
            self.validation_report['suggestions'].insert(0, 
                "🚨 CRÍTICO: Projeto precisa de reestruturação completa para seguir A-SDLC"
            )
        elif score < 70:
            self.validation_report['suggestions'].insert(0,
                "⚠️ ATENÇÃO: Projeto parcialmente conforme, precisa de melhorias"
            )
        elif score < 90:
            self.validation_report['suggestions'].insert(0,
                "✅ BOM: Projeto quase conforme, pequenos ajustes necessários"
            )
        else:
            self.validation_report['suggestions'].insert(0,
                "🎉 EXCELENTE: Projeto totalmente conforme com A-SDLC!"
            )
    
    def generate_report(self, format: str = 'markdown') -> str:
        """
        Gerar relatório de validação formatado
        
        Args:
            format: Formato do relatório ('markdown', 'json', 'text')
            
        Returns:
            Relatório formatado como string
        """
        if format == 'json':
            import json
            return json.dumps(self.validation_report, indent=2, ensure_ascii=False)
        
        elif format == 'markdown':
            return self._generate_markdown_report()
        
        else:  # text
            return self._generate_text_report()
    
    def _generate_markdown_report(self) -> str:
        """Gerar relatório em formato Markdown"""
        report = f"""# 📊 Relatório de Conformidade A-SDLC

**Projeto**: {self.validation_report['project_name']}  
**Data**: {self.validation_report['timestamp']}  
**Score Geral**: {self.validation_report['overall_score']:.1f}/100

## 🎯 Resumo das Validações

| Categoria | Score | Status |
|-----------|-------|--------|
| 📁 Estrutura de Arquivos | {self.validation_report['validations'].get('file_structure', {}).get('score', 0):.1f}/100 | {'✅' if self.validation_report['validations'].get('file_structure', {}).get('score', 0) >= 80 else '❌'} |
| 🤖 Agentes | {self.validation_report['validations'].get('agents', {}).get('score', 0):.1f}/100 | {'✅' if self.validation_report['validations'].get('agents', {}).get('score', 0) >= 80 else '❌'} |
| 📝 Stories | {self.validation_report['validations'].get('stories', {}).get('score', 0):.1f}/100 | {'✅' if self.validation_report['validations'].get('stories', {}).get('score', 0) >= 80 else '❌'} |
| 📋 PROJECT_CONTEXT | {self.validation_report['validations'].get('project_context', {}).get('score', 0):.1f}/100 | {'✅' if self.validation_report['validations'].get('project_context', {}).get('score', 0) >= 80 else '❌'} |
| 📚 Prompts | {self.validation_report['validations'].get('prompts', {}).get('score', 0):.1f}/100 | {'✅' if self.validation_report['validations'].get('prompts', {}).get('score', 0) >= 80 else '❌'} |

## 💡 Sugestões de Melhoria

"""
        for suggestion in self.validation_report['suggestions']:
            report += f"- {suggestion}\n"
        
        if self.validation_report['auto_fix_commands']:
            report += "\n## 🔧 Comandos de Correção Automática\n\n```bash\n"
            for command in self.validation_report['auto_fix_commands']:
                report += f"{command}\n"
            report += "```\n"
        
        return report
    
    def _generate_text_report(self) -> str:
        """Gerar relatório em formato texto simples"""
        report = f"""
📊 RELATÓRIO DE CONFORMIDADE A-SDLC
====================================

Projeto: {self.validation_report['project_name']}
Data: {self.validation_report['timestamp']}
Score Geral: {self.validation_report['overall_score']:.1f}/100

VALIDAÇÕES:
-----------
"""
        for category, data in self.validation_report['validations'].items():
            score = data.get('score', 0) if isinstance(data, dict) else 0
            status = '✅' if score >= 80 else '❌'
            report += f"{category}: {score:.1f}/100 {status}\n"
        
        report += "\nSUGESTÕES:\n----------\n"
        for suggestion in self.validation_report['suggestions']:
            report += f"- {suggestion}\n"
        
        return report


def validate_asdlc_project(project_path: str = '.') -> Dict[str, Any]:
    """
    Função utilitária para validar projeto A-SDLC
    
    Args:
        project_path: Caminho para o projeto (padrão: diretório atual)
        
    Returns:
        Relatório de validação
    """
    validator = ASDLCValidator(Path(project_path))
    return validator.validate_project()


def main():
    """Executar validação via CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validador de Conformidade A-SDLC')
    parser.add_argument('--project', '-p', default='.', 
                       help='Caminho do projeto (padrão: diretório atual)')
    parser.add_argument('--format', '-f', choices=['markdown', 'json', 'text'], 
                       default='markdown', help='Formato do relatório')
    parser.add_argument('--output', '-o', help='Arquivo de saída (padrão: stdout)')
    
    args = parser.parse_args()
    
    # Executar validação
    validator = ASDLCValidator(Path(args.project))
    report = validator.validate_project()
    
    # Gerar relatório formatado
    formatted_report = validator.generate_report(args.format)
    
    # Saída
    if args.output:
        Path(args.output).write_text(formatted_report, encoding='utf-8')
        print(f"📄 Relatório salvo em: {args.output}")
    else:
        print(formatted_report)
    
    # Exit code baseado no score
    exit_code = 0 if report['overall_score'] >= 80 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()