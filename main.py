#!/usr/bin/env python3
"""
A-SDLC Framework - Ponto de Entrada Híbrido (CLI + Interativo)
"""
import argparse
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importa os módulos de lógica
def import_modulos():
    global project_manager, story_manager, ui_manager, find_project_root
    import asdlc.project_manager as project_manager
    import asdlc.story_manager as story_manager
    import asdlc.ui_manager as ui_manager
    from asdlc.utils import find_project_root
import_modulos()

def setup_cli_parser():
    parser = argparse.ArgumentParser(description="A-SDLC Framework")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando: create-project
    p_create = subparsers.add_parser("create-project", help="Cria um novo projeto A-SDLC.")
    p_create.add_argument("--name", required=True, help="Nome do projeto.")
    p_create.add_argument("--prompt", required=True, help="O objetivo de alto nível do projeto.")
    p_create.add_argument("--type", default="web_api", help="Tipo do projeto.")

    # Comando: create-story
    s_create = subparsers.add_parser("create-story", help="Cria uma nova story com plano de execução.")
    s_create.add_argument("--title", required=True, help="Título da story.")
    # Adicionar mais argumentos conforme o story_manager.py evoluir

    # Comando: list-stories
    subparsers.add_parser("list-stories", help="Lista todas as stories do projeto atual.")
    
    # Comando: validate
    v_validate = subparsers.add_parser("validate", help="Valida conformidade A-SDLC do projeto.")
    v_validate.add_argument("--project", "-p", default=".", help="Caminho do projeto (padrão: atual)")
    v_validate.add_argument("--format", "-f", choices=["markdown", "json", "text"], 
                           default="markdown", help="Formato do relatório")
    v_validate.add_argument("--output", "-o", help="Arquivo de saída (padrão: stdout)")
    
    return parser

def execute_cli_command(args):
    if args.command == "create-project":
        project_manager.initialize_project(
            project_name=args.name,
            initial_prompt=args.prompt,
            project_type=args.type
        )
    elif args.command == "create-story":
        story_manager.create_story(story_title=args.title)
    elif args.command == "list-stories":
        story_manager.list_stories()
    elif args.command == "validate":
        from asdlc.validation_checker import ASDLCValidator
        from pathlib import Path
        
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
        return exit_code == 0
    else:
        logger.warning(f"Comando '{args.command}' não reconhecido.")
        return False
    return True

def main():
    """Função principal que decide entre modo CLI e Interativo."""
    parser = setup_cli_parser()
    
    # Adicionar contexto de projeto
    project_root = find_project_root()
    if project_root:
        logger.info(f"📍 Contexto do Projeto Ativo: {project_root.name}")
    else:
        logger.info("📍 Nenhum projeto A-SDLC ativo. Apenas 'create-project' está disponível.")
    
    # Se nenhum argumento (além do nome do script) for passado, entra no modo interativo
    if len(sys.argv) == 1:
        ui = ui_manager.UIManager()
        ui.start_interactive_mode()
    else:
        args = parser.parse_args()
        if not hasattr(args, 'command') or not args.command:
            parser.print_help()
        else:
            execute_cli_command(args)

if __name__ == "__main__":
    main() 