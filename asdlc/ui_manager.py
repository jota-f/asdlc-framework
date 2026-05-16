"""
A-SDLC Framework - Gerenciador de Interface
Responsável pela interface interativa e CLI
"""

import logging
from typing import Optional
from . import utils
from .project_manager import initialize_project
from .story_manager import create_story, list_stories, grill_story_idea, apply_grill_decisions

logger = logging.getLogger(__name__)


class UIManager:
    """Gerenciador de interface do usuário"""

    def __init__(self):
        self.project_manager = None
        self.story_manager = None

    def show_banner(self):
        """Mostra o banner do framework"""
        print("=" * 70)
        print("                    🚀 A-SDLC FRAMEWORK")
        print("              AI-Driven Software Development Lifecycle")
        print("")
        print("  🤖 Agentes de IA • ⚡ Alta Velocidade • 🎯 Alta Qualidade")
        print("=" * 70)

    def show_menu(self):
        """Mostra o menu principal"""
        print("\n📋 MENU A-SDLC - Escolha uma opção:")
        print("")
        print("1. 🚀 Inicializar novo projeto")
        print("2. 📁 Abrir projeto existente")
        print("3. 📝 Criar/Implementar Story")
        print("4. 📋 Listar Stories")
        print("0. ❌ Sair")
        print("")

    def start_interactive_mode(self):
        """Inicia o modo interativo"""
        self.show_banner()

        while True:
            self.show_menu()
            choice = input("🎯 Escolha uma opção: ")

            try:
                self.execute_menu_choice(choice)
                if choice == "0":
                    break
            except KeyboardInterrupt:
                print("\n👋 Saindo...")
                break
            except Exception as e:
                logger.error(f"❌ Erro: {e}")

            print("")
            input("⏸️ Pressione Enter para continuar")
            print("")

    def execute_menu_choice(self, choice: str):
        """Executa a escolha do menu"""
        if choice == "1":
            # Inicializar novo projeto
            project_name = input("📝 Nome do projeto: ")
            initial_prompt = input("🎯 Objetivo de alto nível do projeto: ")
            print("\n🏗️ Tipos de projeto disponíveis:")
            print("1. 🌐 web_frontend - Aplicação web frontend (HTML/CSS/JS)")
            print("2. 🔌 web_api - API web backend (Python/Node.js)")
            print("3. 🌐 web_fullstack - Aplicação web completa (Frontend + Backend)")
            print("4. 📱 mobile - Aplicação móvel (React Native/Flutter)")
            print("5. 💻 desktop - Aplicação desktop (Electron/Tkinter)")
            print("6. 🤖 cli - Aplicação linha de comando")

            type_choice = input("🎯 Escolha o tipo (1-6): ").strip()

            # Mapear escolha para tipo
            type_mapping = {
                "1": "web_frontend",
                "2": "web_api",
                "3": "web_fullstack",
                "4": "mobile",
                "5": "desktop",
                "6": "cli",
            }

            project_type = type_mapping.get(type_choice, "web_frontend")
            print(f"✅ Tipo selecionado: {project_type}")

            if project_name.strip() and initial_prompt.strip():
                initialize_project(project_name, initial_prompt, project_type)
            else:
                logger.error("❌ Nome do projeto e objetivo são obrigatórios.")
        elif choice == "2":
            # Abrir projeto existente - simplificado
            logger.info("💡 Para abrir um projeto existente, navegue até a pasta do projeto e execute os comandos.")
            logger.info("   Exemplo: cd meu-projeto && python ../main.py list-stories")
        elif choice == "3":
            # Criar/Implementar Story
            print("\n📝 CRIAÇÃO DE NOVA STORY")
            print("=" * 40)
            story_title = input("📋 Título da story (ex: 'Implementar Login de Usuário'): ")
            if not story_title.strip():
                logger.error("❌ Título da story é obrigatório.")
                return

            print("\n🎯 DESCRIÇÃO DETALHADA:")
            print("💡 Descreva a funcionalidade em detalhes:")
            print("   - O que deve ser implementado?")
            print("   - Quais são os requisitos específicos?")
            print("   - Que tecnologias devem ser usadas?")
            print("   - Critérios de aceitação importantes?")
            print("")

            story_description = input("📝 Descrição completa da funcionalidade: ")
            if not story_description.strip():
                logger.error("❌ Descrição da funcionalidade é obrigatória.")
                return

            # FASE DE GRILL (Opcional no CLI)
            project_root = utils.find_project_root()
            glossary_path = project_root / "GLOSSARY.md" if project_root else None

            if glossary_path and (not glossary_path.exists() or glossary_path.stat().st_size < 50):
                print("\n⚠️ AVISO: Nenhum GLOSSARY.md válido foi encontrado neste projeto.")
                print("   É altamente recomendado 'grelhar' esta ideia para estabelecer a linguagem de domínio inicial.")

            want_grill = input("\n🔥 Deseja 'grelhar' (grill) esta ideia para validar domínio e arquitetura? (s/n): ").lower()
            if want_grill == "s":
                print("\n🔍 Iniciando Grill...")
                questions = grill_story_idea(story_title, story_description)
                print(f"\n{questions}")
                print("\n💡 Responda às perguntas e forneça detalhes adicionais abaixo (ou 'pular'):")
                answers = input("📝 Respostas: ")

                if answers.lower() != "pular":
                    discussion = f"Título: {story_title}\nDescrição Original: {story_description}\nPerguntas: {questions}\nRespostas: {answers}"
                    apply_grill_decisions(discussion)
                    print("✅ Glossário e ADRs atualizados com base na discussão.")

                    # Atualizar descrição com as respostas para a criação da story
                    story_description = f"{story_description}\n\nDetalhamento do Grill:\n{answers}"

            # Criar story com título e descrição (final)
            create_story(story_title=story_title, story_description=story_description)
        elif choice == "4":
            # Listar Stories
            list_stories()
        elif choice == "0":
            logger.info("👋 Obrigado por usar o A-SDLC Framework!")
        else:
            logger.error("❌ Opção inválida. Tente novamente.")
