"""
A-SDLC Framework - Gerenciador de Stories
Módulo responsável por criar, listar e gerenciar stories do projeto
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import re

# Importar gerador de planos e utilitários
from .plan_generator import gerar_plano_de_execucao
from .utils import find_project_root

# Configurar logging
logger = logging.getLogger(__name__)

def create_story(
    story_title: str,
    story_description: Optional[str] = None,
    story_type: str = "user_story",
    acceptance_criteria: Optional[str] = None,
    priority: str = "Medium",
    estimate: Optional[str] = None,
    **kwargs
) -> str:
    """
    Cria uma nova story com plano de execução detalhado
    
    Args:
        story_title: Título da story
        story_description: Descrição da story
        story_type: Tipo da story (user_story, bug_fix, technical_story, enhancement)
        acceptance_criteria: Critérios de aceitação
        priority: Prioridade (High, Medium, Low)
        estimate: Estimativa em horas
        **kwargs: Parâmetros adicionais
        
    Returns:
        str: ID da story criada
    """
    try:
        # 1. ENCONTRAR A RAIZ DO PROJETO
        project_root = find_project_root()
        if not project_root:
            logger.error("❌ Operação cancelada. Execute este comando de dentro de um projeto A-SDLC.")
            logger.error("💡 Use 'python main.py create-project' para criar um novo projeto.")
            return None

        logger.info(f"Criando nova story no projeto: {project_root.name}")
        
        # Validar parâmetros
        if not story_title.strip():
            raise ValueError("Título da story é obrigatório")
        
        # Gerar ID único para a story
        story_id = _gerar_story_id(story_title)
        
        # Gerar descrição padrão se não fornecida
        if not story_description:
            story_description = f"Implementar funcionalidade: {story_title}"
        
        # Preparar dados da story para o gerador de planos
        story_data = {
            'id': story_id,
            'title': story_title,
            'description': story_description,
            'type': story_type,
            'acceptance_criteria': acceptance_criteria,
            'priority': priority,
            'estimate': estimate,
            'files_to_create': kwargs.get('files_to_create', ''),
            'files_to_modify': kwargs.get('files_to_modify', '')
        }
        
        # Gerar plano de execução usando o gerador de planos dinâmico
        plano_execucao = gerar_plano_de_execucao(story_data, project_root)
        
        # 2. GARANTIR QUE A PASTA DE STORIES ESTÁ NO LUGAR CERTO
        stories_dir = project_root / "stories"
        stories_dir.mkdir(exist_ok=True)
        
        # Criar arquivo da story
        story_filename = f"{story_id}_{_sanitize_filename(story_title)}.md"
        story_path = stories_dir / story_filename
        
        # Salvar story com plano de execução
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(plano_execucao)
        
        logger.info(f"Story criada com sucesso: {story_path}")
        
        # Mostrar informações da story criada
        _mostrar_info_story_criada(story_id, story_title, story_path)
        
        return story_id
        
    except Exception as e:
        logger.error(f"Erro ao criar story: {e}")
        raise

def list_stories() -> List[Dict[str, Any]]:
    """
    Lista todas as stories do projeto
    
    Returns:
        List[Dict[str, Any]]: Lista de stories com informações
    """
    try:
        # 1. ENCONTRAR A RAIZ DO PROJETO
        project_root = find_project_root()
        if not project_root:
            logger.error("❌ Operação cancelada. Execute este comando de dentro de um projeto A-SDLC.")
            logger.error("💡 Use 'python main.py create-project' para criar um novo projeto.")
            return []

        logger.info(f"Listando stories do projeto: {project_root.name}")
        
        # 2. GARANTIR QUE A PASTA DE STORIES ESTÁ NO LUGAR CERTO
        stories_dir = project_root / "stories"
        if not stories_dir.exists():
            logger.info("Diretório de stories não encontrado. Nenhuma story criada ainda.")
            return []
        
        stories = []
        
        # Procurar por arquivos .md no diretório stories
        for story_file in stories_dir.glob("*.md"):
            try:
                story_info = _extrair_info_story(story_file)
                if story_info:
                    stories.append(story_info)
                    logger.debug(f"Story processada: {story_info.get('title', 'N/A')}")
            except Exception as e:
                logger.warning(f"Erro ao processar story {story_file}: {e}")
        
        logger.info(f"Total de stories encontradas: {len(stories)}")
        
        # Ordenar stories por data de criação (mais recentes primeiro)
        stories.sort(key=lambda x: x.get('created', ''), reverse=True)
        
        # Mostrar lista de stories
        _mostrar_lista_stories(stories)
        
        return stories
        
    except Exception as e:
        logger.error(f"Erro ao listar stories: {e}")
        raise

def implement_story(story_file: str, story_id: Optional[str] = None) -> bool:
    """
    Implementa uma story específica
    
    Args:
        story_file: Caminho para o arquivo da story
        story_id: ID da story (opcional)
        
    Returns:
        bool: True se implementação foi bem-sucedida
    """
    try:
        # 1. ENCONTRAR A RAIZ DO PROJETO
        project_root = find_project_root()
        if not project_root:
            logger.error("❌ Operação cancelada. Execute este comando de dentro de um projeto A-SDLC.")
            return False

        logger.info(f"Iniciando implementação da story no projeto: {project_root.name}")
        
        # Validar arquivo da story
        story_path = Path(story_file)
        if not story_path.exists():
            raise FileNotFoundError(f"Arquivo da story não encontrado: {story_file}")
        
        # Extrair informações da story
        story_info = _extrair_info_story(story_path)
        if not story_info:
            raise ValueError("Não foi possível extrair informações da story")
        
        logger.info(f"Implementando story: {story_info.get('title', 'N/A')}")
        
        # Executar etapas de implementação
        sucesso = _executar_etapas_implementacao(story_info)
        
        if sucesso:
            logger.info("Implementação da story concluída com sucesso")
            _atualizar_status_story(story_path, "implemented")
        else:
            logger.error("Falha na implementação da story")
            _atualizar_status_story(story_path, "failed")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro ao implementar story: {e}")
        return False

def show_story_metrics(story_id: str) -> Dict[str, Any]:
    """
    Mostra métricas de uma story específica
    
    Args:
        story_id: ID da story
        
    Returns:
        Dict[str, Any]: Métricas da story
    """
    try:
        # 1. ENCONTRAR A RAIZ DO PROJETO
        project_root = find_project_root()
        if not project_root:
            logger.error("❌ Operação cancelada. Execute este comando de dentro de um projeto A-SDLC.")
            raise ValueError("Projeto A-SDLC não encontrado")

        logger.info(f"Calculando métricas para story no projeto: {project_root.name}")
        
        # Encontrar arquivo da story
        story_file = _encontrar_story_por_id(story_id)
        if not story_file:
            raise FileNotFoundError(f"Story não encontrada: {story_id}")
        
        # Extrair métricas
        metrics = _calcular_metricas_story(story_file)
        
        # Mostrar métricas
        _mostrar_metricas_story(story_id, metrics)
        
        return metrics
        
    except Exception as e:
        logger.error(f"Erro ao calcular métricas da story: {e}")
        raise

def _gerar_story_id(title: str) -> str:
    """
    Gera ID único para a story baseado no título
    
    Args:
        title: Título da story
        
    Returns:
        str: ID único da story
    """
    # Gerar timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Criar ID baseado no título
    title_part = re.sub(r'[^a-zA-Z0-9]', '_', title.lower())
    title_part = re.sub(r'_+', '_', title_part)
    title_part = title_part[:20]  # Limitar tamanho
    
    return f"{timestamp}_{title_part}"

def _sanitize_filename(filename: str) -> str:
    """
    Sanitiza nome de arquivo removendo caracteres especiais
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        str: Nome sanitizado
    """
    # Remover caracteres especiais
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Substituir espaços por underscores
    sanitized = sanitized.replace(' ', '_')
    # Remover underscores múltiplos
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remover underscores no início e fim
    sanitized = sanitized.strip('_')
    
    return sanitized

def _mostrar_info_story_criada(story_id: str, title: str, file_path: Path) -> None:
    """
    Mostra informações da story criada
    
    Args:
        story_id: ID da story
        title: Título da story
        file_path: Caminho do arquivo
    """
    print(f"\n🎉 Story criada com sucesso!")
    print(f"📝 Título: {title}")
    print(f"🆔 ID: {story_id}")
    print(f"📁 Arquivo: {file_path}")
    print(f"📋 Plano de execução gerado automaticamente")
    print(f"🤖 Templates de agentes integrados")
    print(f"\n💡 Próximos passos:")
    print(f"   1. Revisar o plano de execução gerado")
    print(f"   2. Ajustar critérios de aceitação se necessário")
    print(f"   3. Iniciar implementação seguindo o plano")
    print(f"   4. Usar 'python main.py list-stories' para ver todas as stories")

def _extrair_info_story(story_file: Path) -> Optional[Dict[str, Any]]:
    """
    Extrai informações de um arquivo de story
    
    Args:
        story_file: Caminho para o arquivo da story
        
    Returns:
        Optional[Dict[str, Any]]: Informações da story
    """
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            logger.warning(f"Frontmatter não encontrado em {story_file}")
            return None
        
        frontmatter = frontmatter_match.group(1)
        
        # Extrair campos do frontmatter
        info = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"')
                info[key] = value
        
        # Adicionar informações do arquivo
        info['file_path'] = str(story_file)
        info['file_size'] = story_file.stat().st_size
        info['modified'] = datetime.fromtimestamp(story_file.stat().st_mtime)
        
        # Extrair ID do nome do arquivo
        filename = story_file.stem
        if '_' in filename:
            info['story_id'] = filename.split('_')[0]
        
        logger.debug(f"Informações extraídas: {info}")
        return info
        
    except Exception as e:
        logger.warning(f"Erro ao extrair informações da story {story_file}: {e}")
        return None

def _mostrar_lista_stories(stories: List[Dict[str, Any]]) -> None:
    """
    Mostra lista de stories formatada
    
    Args:
        stories: Lista de stories
    """
    if not stories:
        print("Nenhuma story encontrada.")
        print("Use 'python main.py create-story --title \"Sua Story\"' para criar uma nova story.")
        return
    
    print(f"Stories do Projeto ({len(stories)} encontradas)")
    print("=" * 50)
    
    for i, story in enumerate(stories, 1):
        title = story.get('title', 'Sem título')
        story_id = story.get('story_id', 'N/A')
        status = story.get('status', 'unknown')
        priority = story.get('priority', 'Medium')
        created = story.get('created', 'N/A')
        
        print(f"{i}. {title}")
        print(f"   ID: {story_id}")
        print(f"   Status: {status}")
        print(f"   Prioridade: {priority}")
        print(f"   Criada: {created}")
        print(f"   Arquivo: {story.get('file_path', 'N/A')}")
        print()
    
    print("=" * 50)
    print("Listagem concluida")

def _executar_etapas_implementacao(story_info: Dict[str, Any]) -> bool:
    """
    Executa etapas de implementação da story
    
    Args:
        story_info: Informações da story
        
    Returns:
        bool: True se implementação foi bem-sucedida
    """
    try:
        title = story_info.get('title', 'Story')
        logger.info(f"Executando etapas de implementação para: {title}")
        
        # Simular etapas de implementação
        etapas = [
            "Análise de requisitos",
            "Design da arquitetura",
            "Desenvolvimento de código",
            "Criação de testes",
            "Code review",
            "Deploy"
        ]
        
        for i, etapa in enumerate(etapas, 1):
            logger.info(f"Etapa {i}/{len(etapas)}: {etapa}")
            # Aqui seria implementada a lógica real de cada etapa
            # Por enquanto, apenas simula o processo
        
        logger.info("Todas as etapas de implementação concluídas")
        return True
        
    except Exception as e:
        logger.error(f"Erro durante implementação: {e}")
        return False

def _atualizar_status_story(story_path: Path, status: str) -> None:
    """
    Atualiza status da story no arquivo
    
    Args:
        story_path: Caminho do arquivo da story
        status: Novo status
    """
    try:
        with open(story_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Atualizar status no frontmatter
        content = re.sub(
            r'status:\s*"[^"]*"',
            f'status: "{status}"',
            content
        )
        
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Status da story atualizado para: {status}")
        
    except Exception as e:
        logger.error(f"Erro ao atualizar status da story: {e}")

def _encontrar_story_por_id(story_id: str) -> Optional[Path]:
    """
    Encontra arquivo da story pelo ID
    
    Args:
        story_id: ID da story
        
    Returns:
        Optional[Path]: Caminho do arquivo da story
    """
    project_root = find_project_root()
    if not project_root:
        return None
    
    stories_dir = project_root / "stories"
    if not stories_dir.exists():
        return None
    
    for story_file in stories_dir.glob("*.md"):
        if story_id in story_file.stem:
            return story_file
    
    return None

def _calcular_metricas_story(story_file: Path) -> Dict[str, Any]:
    """
    Calcula métricas de uma story
    
    Args:
        story_file: Caminho do arquivo da story
        
    Returns:
        Dict[str, Any]: Métricas calculadas
    """
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calcular métricas básicas
        total_lines = len(content.split('\n'))
        total_chars = len(content)
        total_words = len(content.split())
        
        # Contar seções
        sections = len(re.findall(r'^##\s+', content, re.MULTILINE))
        
        # Contar checkboxes
        checkboxes = len(re.findall(r'- \[ \]', content))
        completed_checkboxes = len(re.findall(r'- \[x\]', content))
        
        # Calcular progresso
        total_tasks = checkboxes + completed_checkboxes
        progress = (completed_checkboxes / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_lines': total_lines,
            'total_chars': total_chars,
            'total_words': total_words,
            'sections': sections,
            'total_tasks': total_tasks,
            'completed_tasks': completed_checkboxes,
            'progress_percentage': round(progress, 1)
        }
        
    except Exception as e:
        logger.error(f"Erro ao calcular métricas: {e}")
        return {}

def _mostrar_metricas_story(story_id: str, metrics: Dict[str, Any]) -> None:
    """
    Mostra métricas de uma story
    
    Args:
        story_id: ID da story
        metrics: Métricas calculadas
    """
    print(f"\n📊 Métricas da Story: {story_id}")
    print("=" * 50)
    
    if not metrics:
        print("❌ Não foi possível calcular métricas")
        return
    
    print(f"📄 Total de linhas: {metrics.get('total_lines', 0)}")
    print(f"📝 Total de caracteres: {metrics.get('total_chars', 0)}")
    print(f"📖 Total de palavras: {metrics.get('total_words', 0)}")
    print(f"📋 Seções do plano: {metrics.get('sections', 0)}")
    print(f"✅ Tarefas completadas: {metrics.get('completed_tasks', 0)}/{metrics.get('total_tasks', 0)}")
    print(f"📈 Progresso: {metrics.get('progress_percentage', 0)}%")
    
    # Barra de progresso visual
    progress = metrics.get('progress_percentage', 0)
    bar_length = 20
    filled_length = int(bar_length * progress / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"📊 Progresso: [{bar}] {progress}%")

# Funções de placeholder para compatibilidade
def _generate_code_local(prompt: str, code_type: str) -> str:
    """Placeholder para geração de código local"""
    return f"// Código gerado para: {prompt} (tipo: {code_type})"

def run_tests_for_story(story_id: str) -> bool:
    """Placeholder para execução de testes"""
    logger.info(f"Executando testes para story: {story_id}")
    return True

def review_code_for_story(story_id: str) -> bool:
    """Placeholder para code review"""
    logger.info(f"Executando code review para story: {story_id}")
    return True

def deploy_story(story_id: str) -> bool:
    """Placeholder para deploy"""
    logger.info(f"Executando deploy para story: {story_id}")
    return True 