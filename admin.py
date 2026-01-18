from rich.console import Console
from rich.table import Table

from database import JsonDatabase

console = Console()
db = JsonDatabase("database.json") 
wh = JsonDatabase("withdrawals.json")

def admin_menu():
    table = Table(title="Admin Menu", header_style="bold red")
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Action", style="green")

    table.add_row("1", "View All Accounts")
    table.add_row("2", "View All Transactions")
    table.add_row("3", "Manage Accounts")
    table.add_row("4", "View Total Bank Balance")
    table.add_row("5", "Logout")

    console.print(table)