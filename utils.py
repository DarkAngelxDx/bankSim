from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def welcome_screen():
    console.print(Panel.fit(
        "[bold cyan]Welcome to the Bank Simulator[/bold cyan]\n"
        "[green]Secure • Simple • Fast[/green]",
        title="🏦 BANK",
        border_style="blue"
    ))

def main_menu():
    table = Table(title="Main Menu", show_header=True, header_style="bold magenta")

    table.add_column("Option", style="cyan", justify="center")
    table.add_column("Action", style="green")

    table.add_row("1", "Create Account")
    table.add_row("2", "Login")
    table.add_row("3", "Exit")

    console.print(table)