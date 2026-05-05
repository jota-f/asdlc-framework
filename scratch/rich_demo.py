from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
import time

console = Console()

def demo_feedback():
    console.print(Panel.fit("[bold blue]A-SDLC Framework v2.5[/bold blue] - [italic]Iniciando Pipeline...[/italic]", border_style="bright_blue"))
    
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        # Etapa 1
        t1 = progress.add_task(description="[cyan]Agente Architecture:[/cyan] Desenhando solução...", total=None)
        time.sleep(2)
        progress.update(t1, description="[green]Agente Architecture:[/green] Design Concluído! ✅")
        time.sleep(0.5)
        
        # Etapa 2
        t2 = progress.add_task(description="[yellow]Agente Code:[/yellow] Implementando lógica...", total=None)
        time.sleep(3)
        progress.update(t2, description="[green]Agente Code:[/green] Código Gerado! 🚀")
        time.sleep(0.5)
        
        # Etapa 3
        t3 = progress.add_task(description="[magenta]Agente Review:[/magenta] Kimi 2.6 analisando segurança...", total=None)
        time.sleep(2.5)
        progress.update(t3, description="[green]Agente Review:[/green] Revisão Aprovada! 💎")

    console.print("\n[bold green]✨ Pipeline concluído com sucesso![/bold green]\n")

if __name__ == "__main__":
    demo_feedback()
