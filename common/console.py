"""
Rich console helper.
"""

from rich.console import Console
from rich.panel import Panel

from config.config import settings

console = Console()

def title(text: str) -> None:
    if settings.debug:
        print("--> Entering console.title")

    console.print(
        Panel.fit(
            text,
            style="bold cyan"
        )
    )

    if settings.debug:
        print("<-- Exiting console.title")

def section(text: str) -> None:
    console.rule(f"[bold yellow]{text}")

def success(text: str) -> None:
    console.print(f"[green]✓ {text}[/green]")

def warning(text: str) -> None:
    console.print(f"[yellow]! {text}[/yellow]")

def error(text: str) -> None:
    console.print(f"[bold red]✗ {text}[/bold red]")
