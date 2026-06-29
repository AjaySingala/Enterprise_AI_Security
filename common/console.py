"""
Rich console helper.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

def title(text: str) -> None:
    print("--> Entering console.title")

    console.print(
        Panel.fit(
            text,
            style="bold cyan"
        )
    )

    print("<-- Exiting console.title")

def section(text: str) -> None:
    console.rule(f"[bold yellow]{text}")

def success(text: str) -> None:
    console.print(f"[green]✓ {text}[/green]")

def warning(text: str) -> None:
    console.print(f"[yellow]! {text}[/yellow]")

def error(text: str) -> None:
    console.print(f"[bold red]✗ {text}[/bold red]")
