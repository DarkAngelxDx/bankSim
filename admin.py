from typing import Any
from rich.console import Console
from rich.table import Table

from database import JsonDatabase

console = Console()
db = JsonDatabase("database.json") 
wh = JsonDatabase("withdrawals.json")

def admin_menu():
    while True:
        table = Table(title="Admin Menu", header_style="bold red")
        table.add_column("Option", justify="center", style="cyan")
        table.add_column("Action", style="green")

        table.add_row("1", "View All Accounts")
        table.add_row("2", "View All Transactions")
        table.add_row("3", "Manage Accounts")
        table.add_row("4", "View Total Bank Balance")
        table.add_row("5", "Search Accounts")
        table.add_row("6", "Logout")

        console.print(table)

        choice = input("Choose an option: ")

        if choice == "1":
            accounts = db.read()
            account_table = Table(title="All Accounts", header_style="bold blue")
            account_table.add_column("Name", style="cyan")
            account_table.add_column("Balance", style="green")
            account_table.add_column("Account Info", style="yellow")

            for acc in accounts:
                account_table.add_row(acc["name"], str(acc.get("balance", 0)), str(acc.get("created_at", "Unknown")))

            console.print(account_table)

        elif choice == "2":
            transactions = wh.read()
            transaction_table = Table(title="All Transactions", header_style="bold magenta")
            transaction_table.add_column("Account", style="cyan")
            transaction_table.add_column("Type", style="green")
            transaction_table.add_column("Amount", style="yellow")
            transaction_table.add_column("Date", style="white")

            tx_type = input("Enter type (deposit/withdraw): ").lower()
            filtered: list[Any] = [t for t in wh.read() if t.get("type") == tx_type]


            for trans in transactions:
                transaction_table.add_row(
                    trans.get("account", "Unknown"),
                    trans.get("type", "Unknown"),           
                    str(trans.get("amount", 0)),
                    trans.get("date", "Unknown")
                )

            console.print(transaction_table)

        elif choice == "3":
            name = input("Enter account name to manage: ")
            account = db.find_by_name(name)
            if not account:
                console.print(f"[red]Account '{name}' not found.[/red]")
            else:
                new_balance = float(input(f"Enter new balance for {name} (current: {account.get('balance', 0)}): "))
                account["balance"] = new_balance
                db.update_account(account)
                console.print(f"[green]Account '{name}' updated successfully.[/green]")

        elif choice == "4":
            accounts = db.read()
            total_balance = sum(acc.get("balance", 0) for acc in accounts)
            console.print(f"[bold yellow]Total Bank Balance:[/bold yellow] ${total_balance}")

        elif choice == "5":
            name = input("Enter account name to search: ").lower()
            accounts = db.read()
            results = [acc for acc in accounts if name in acc["name"].lower()]
            if not results:
                console.print(f"[red]Account '{name}' not found.[/red]")
            else:
                console.print(f"[green]Account Found:[/green] Name: {results[0]['name']}, Balance: {results[0].get('balance', 0)}, Created At: {results[0].get('created_at', 'Unknown')}")

        elif choice == "6":
            console.print("Logging out...")
            break