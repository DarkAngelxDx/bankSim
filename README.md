# 🏦 Bank Simulator

### *A Modern CLI Banking System Built with Python & Rich*

A clean, interactive **command-line banking simulator** written in Python.
This project mimics real-world banking operations using **JSON-based persistence** and a **Rich-powered terminal UI** for a modern, user-friendly experience.

> 🎯 Built as a learning + portfolio project to practice authentication, data persistence, and CLI UX design.

---

## ✨ Key Features

### 👤 User Accounts

* Create and login to accounts
* Hidden password input (`getpass`)
* Unique usernames (no duplicates)
* Account creation timestamp

### 💳 Banking Operations

* Deposit money
* Withdraw money
* Send money to other users
* Real-time balance updates
* Account information display

### 📜 Transaction History

* Stores withdrawals and transfers
* Persistent JSON storage
* Displayed in **Rich tables**
* Shows latest transactions clearly

### 🎨 Rich Terminal UI

* Colored menus and prompts
* Panels and tables
* Input validation
* Loading spinners
* Clean and readable output

### ⚙️ Other Services (Preview)

* Loan system *(coming soon)*
* Savings accounts *(coming soon)*
* Credit score *(coming soon)*
* Styled with Rich panels and progress indicators

---

## 🧰 Tech Stack

* **Python 3**
* **Rich** — modern CLI UI
* **JSON** — lightweight data storage
* **getpass** — secure password input

---

## 📂 Project Structure

```
.
├── main.py               # Main application
├── database.json         # User accounts data
├── withdrawals.json      # Transactions history
└── README.md             # Documentation
```

---

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install rich
```

### 2️⃣ Run the application

```bash
python main.py
```

---

## 🖥️ How It Works

1. Launch the program
2. Create a new account or log in
3. Access banking features:

   * Deposits & withdrawals
   * Transfers between users
   * Transaction history
   * Account details
4. All data is saved automatically in JSON files
5. Rich handles all UI elements

---

## 🔐 Security Notes

* Passwords are hidden during input
* Currently stored as plain text
  🔧 **Planned improvement:** password hashing (SHA-256)

---

## 🛠️ Planned Improvements

* 🔐 Password hashing
* 💸 Full transaction history (deposits + withdrawals)
* 🏦 Loan & interest system
* 🛂 Admin panel
* 💱 Multi-currency support
* 🧱 OOP refactor
* 📤 Export transactions (CSV / TXT)

---

## 🎯 Why This Project?

This project demonstrates:

* Practical Python programming
* File-based persistence
* CLI application design
* Real-world logic simulation
* Clean, readable code structure

Perfect for:

* Learning purposes
* Portfolio showcase
* Base for more advanced systems

---

## 👨‍💻 Author

Developed by **Maks**
Built with curiosity, practice, and attention to detail 🚀

---


