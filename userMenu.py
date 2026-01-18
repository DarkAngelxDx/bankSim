from rich.table import Table
from rich.console import Console
from UserFunc import deposit, withdraw, send_money, balance, account_info, other
from UserFunc import transaction_history

console = Console()

def user_menu(account):
    while True:
        table = Table(title=f"Welcome, {account['name']}")
        table.add_column("Option")
        table.add_column("Action")
        table.add_row("1", "Deposit")
        table.add_row("2", "Withdraw")
        table.add_row("3", "Check Balance")
        table.add_row("4", "Account Info")
        table.add_row("5", "Transaction History")
        table.add_row("6", "Send Money")
        table.add_row("7", "Other Services")
        table.add_row("8", "Logout")
        console.print(table)

        choice = input("Choose option: ")

        if choice == "1":
            deposit(account)
        elif choice == "2":
            withdraw(account)
        elif choice == "3":
            balance(account)
        elif choice == "4":
            account_info(account)
        elif choice == "5":
            transaction_history(account)
        elif choice == "6":
            send_money(account)
        elif choice == "7":
            other()
        elif choice == "8":
            break
