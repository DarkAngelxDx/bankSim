from utils import welcome_screen, main_menu
from UserFunc import register_account, login
from userMenu import user_menu
from admin import admin_menu
from database import JsonDatabase

db = JsonDatabase("database.json")



welcome_screen()
main_menu()
choice = input("Choose option: ")

if choice == "1":
    register_account()

elif choice == "2":
    account = login()
    if account:
        user_menu(account)

elif choice == "admin":
    admin_menu()

elif choice == "3":
    print("Goodbye")

