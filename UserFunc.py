import datetime 
from rich.console import Console 
from database import JsonDatabase
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt
import getpass

console = Console()

db = JsonDatabase("database.json") 
wh = JsonDatabase("withdrawals.json")

def create_account(name, password, date):
    return {
        "name": name, 
        "password": password, 
        "balance": 0.0, 
        "created_at": date["created_at"]
        } 

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
        print("Account not found.")
        return None

    password = getpass.getpass("Password: ")

    if account["password"] != password:
        print("Incorrect password.")
        return None

    if "created_at" not in account:
        account["created_at"] = "Unknown"
        db.update_account(account)

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


def send_money(account):
    name = input("Choose recipient: ")
    recipient = db.find_by_name(name)

    if recipient is None:
        print("Account not found.")
        return

    amount = float(input("Enter amount to send: "))

    if amount <= 0:
        print("Amount must be positive.")
        return

    if amount > account.get('balance', 0):
        print("Insufficient funds.")
        return

    # SAFETY: ensure balance exists
    recipient['balance'] = recipient.get('balance', 0)

    account['balance'] -= amount
    recipient['balance'] += amount

    db.update_account(account)
    db.update_account(recipient)

    wh.add({
        "account": account['name'],
        "amount": amount,
        "type": "send_money",
        "to": name,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    print(f"Sent {amount} to {name}. New balance: {account['balance']}")



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
        datetime.time.sleep(2)

    console.print(
        Panel(
            "[bold red]This feature is not available yet.[/bold red]\n"
            "[white]Stay tuned for future updates![/white]",
            title="🚧 Under Development",
            border_style="red"
        )
    )

def transaction_history(account):

    table = Table(title="Withdrawal History", header_style="bold yellow")
    table.add_column("#", justify="center")
    table.add_column("Amount", justify="right")
    table.add_column("Date")
 
    all_transaction = wh.read()
    transaction = [w for w in all_transaction if w.get('account') == account['name']]

    if not transaction:
         console.print("[red]No withdrawals found[/red]")
         return

    else:
        for i, trans in enumerate(transaction[-10:], 1):
            trans_type = trans.get('type', 'unknown')
            table.add_row(f"{i}. {trans_type} ${trans.get('amount', 0)} on {trans.get('date', 'N/A')}")

    console.print(table)

def balance(account):
    print(f"Your current balance is: {account.get('balance', 0)}")

def account_info(account):
    info = (
        f"[bold cyan]Name:[/bold cyan] {account['name']}\n"
        f"[bold cyan]Balance:[/bold cyan] {account['balance']}"
        f'\n[bold cyan]Account Created At:[/bold cyan] {account["created_at"]}'
    )

    console.print(Panel(info, title="Account Info", border_style="green"))