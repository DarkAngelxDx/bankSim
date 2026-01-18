import json
import os
import datetime
import getpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt
from rich.text import Text
from typing import Any, List
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
console = Console()


# Simple JSON-based database handler
class JsonDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def read(self) -> List[Any]:
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def add(self, data: dict):
        db = self.read()
        db.append(data)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    def find_by_name(self, name: str):
        db = self.read()
        for acc in db:
            if acc["name"] == name:
                return acc
        return None

    def update_account(self, updated_account):
        db = self.read()
        for i, acc in enumerate(db):
            if acc["name"] == updated_account["name"]:
                db[i] = updated_account
                break
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)


db = JsonDatabase("database.json") # main user database
wh = JsonDatabase("withdrawals.json") # withdrawal history database

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

def user_menu(account_name):
    table = Table(title=f"Welcome, {account_name}", header_style="bold cyan")
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Action", style="green")

    table.add_row("1", "Deposit")
    table.add_row("2", "Withdraw")
    table.add_row("3", "Check Balance")
    table.add_row("4", "Account Info")
    table.add_row("5", "Transaction History")
    table.add_row("6", "Send Money")
    table.add_row("7", "Other Services")
    table.add_row("8", "Logout")

    console.print(table)


def create_account(name, password, date):
    return {"name": name, "password": password, "balance": 0.0, "created_at": date["created_at"]}


def register_account():
    name = input("write your name: ")
    if len(name) < 1:
        print("Name cannot be empty. Please try again.")
        return
    elif db.find_by_name(name) is not None:  
        print("Account with this name already exists. Please write other name.")
        return
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm your password: ")

    if password != password_confirm:
        print("Passwords do not match. Please try again.")
        return
    
    date = {"created_at": datetime.datetime.now().isoformat()}

    account = create_account(name, password, date)
    db.add(account)
    print(f"Account created successfully for {name}!")


def login():
    name = input("write your name: ")
    account = db.find_by_name(name)

    if account is None:
        print("Account not found. Please try again.")
        return None

    password = getpass.getpass("Password: ")

    if account["password"] != password:
        print("Incorrect password. Please try again.")
        return None

    print(f"Welcome back, {account['name']}!")
    return account


def deposit(account):
    amount = FloatPrompt.ask("Enter amount to deposit")

    if amount <= 0:
        console.print("[red]Amount must be greater than zero[/red]")
        return

    account['balance'] += amount
    db.update_account(account)

    console.print(f"[green]✔ Deposited {amount}[/green]")
    console.print(f"[bold cyan]New balance:[/bold cyan] {account['balance']}")


def withdraw(account):
    amount = FloatPrompt.ask("Enter amount to withdraw")

    if amount <= 0:
        console.print("[red]Invalid amount[/red]")
        return

    if amount > account['balance']:
        console.print("[bold red]✖ Insufficient funds[/bold red]")
        return

    account['balance'] -= amount
    db.update_account(account)

    wh.add({
        "account": account['name'],
        "amount": amount,
        "type": "withdraw",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    console.print("[green]✔ Withdrawal successful[/green]")


def send_money():
    name = input("choose recipient: ")
    recipient = db.find_by_name(name)
    if recipient is None:
        print("Account not found. Please try again.")
        return
    amount = float(input("Enter amount to send: "))
    if amount > account.get('balance', 0):
        print("Insufficient funds.")
    elif amount <= 0:
        print("Amount must be positive.")
    else:
        account['balance'] -= amount
        recipient['balance'] += amount
        print(f"Sent {amount} to {name}. New balance is {account['balance']}.")
        db.update_account(account)
        db.update_account(recipient)
        wh.add({
            "account": account['name'],
            "amount": amount,
            "type": "send_money",
            "to": name,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


def other():
    console.print(Panel(
        "[bold yellow]Additional Services[/bold yellow]\n"
        "[cyan]More banking features coming soon[/cyan]",
        title="⚙ Other Services",
        border_style="yellow"
    ))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Feature", style="green")
    table.add_column("Status", style="yellow")

    table.add_row("1", "Loan System", "🚧 In development")
    table.add_row("2", "Savings Account", "🚧 In development")
    table.add_row("3", "Credit Score", "🚧 In development")
    table.add_row("4", "Back", "↩")

    console.print(table)

    choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4"])

    if choice == "4":
        return

    # Fake loading animation for unavailable features
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Loading feature...", total=None)
        time.sleep(2)

    console.print(
        Panel(
            "[bold red]This feature is not available yet.[/bold red]\n"
            "[white]Stay tuned for future updates![/white]",
            title="🚧 Under Development",
            border_style="red"
        )
    )


def balance(account):
    print(f"Your current balance is: {account.get('balance', 0)}")


transaction_types = {
    0: "withdraw", 
    1: "send_money", 
    2: "deposit", 
    3: "other"
    }


def transaction_history():
    table = Table(
        title="Transaction History",
        header_style="bold yellow"
    )

    table.add_column("#", justify="center")
    table.add_column("Transaction Type", justify="center")
    table.add_column("Amount", justify="right")
    table.add_column("From / To", justify="center")
    table.add_column("Date")

    all_transactions = wh.read()
    username = account['name']

    transactions = [
        t for t in all_transactions
        if t.get('account') == username or t.get('to') == username
    ]

    if not transactions:
        console.print("[red]No transactions found[/red]")
        return

    for i, trans in enumerate(transactions[-10:], 1):
        type_id = trans.get('type', 3)  # default = other
        type_name = transaction_types.get(type_id, "unknown")

        amount = trans.get('amount', 0)
        date = trans.get('date', 'N/A')

        if trans.get('account') == username:
            # sent 
            direction = f"→ {trans.get('to', '{account}')}"
            flow = "SEND"
        else:
            # rec 
            direction = f"← {trans.get('account', '{sender}')}"
            flow = "RECEIVE"

        table.add_row(
            str(i),
            f"{type_name} ({flow})",
            f"${amount}",
            direction,
            date
        )

    console.print(table)



def account_info(account):
    info = (
        f"[bold cyan]Name:[/bold cyan] {account['name']}\n"
        f"[bold cyan]Balance:[/bold cyan] {account['balance']}"
        f'\n[bold cyan]Account Created At:[/bold cyan] {account["created_at"]}'
    )

    console.print(Panel(info, title="Account Info", border_style="green"))


# Main program 

while True:
    welcome_screen()
    main_menu()
    choice = Prompt.ask("Choose option", choices=["1", "2", "3"])


    if choice == '1':
        register_account()

    elif choice == '2':

        account = login()
        if account is not None:
            logged_in = True
            while logged_in:
                user_menu(account['name'])
                sub_choice = Prompt.ask(
                    "Choose option",
                    choices=["1", "2", "3", "4", "5", "6", "7", "8"]
                )

                if sub_choice == '1':
                    deposit(account)
                    
                elif sub_choice == '2':
                    withdraw(account)

                elif sub_choice == '3':
                    balance(account)

                elif sub_choice == '4':
                    account_info(account)
                        
                elif sub_choice == '5':
                    print("Checking transaction history...")
                    transaction_history()

                elif sub_choice == '6':
                    send_money()

                elif sub_choice == '7':
                    other()

                elif sub_choice == '8':
                    print("Logout")
                    logged_in = False
                    
        else:
            print("Login failed. Please try again.")
            continue
    elif choice == '3':
        print("Thank you for using the Bank Simulator. Goodbye!")
        break