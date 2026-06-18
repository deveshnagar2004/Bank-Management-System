import tkinter as tk
import json
from tkinter import messagebox ,ttk
from bank import (
    Account,
    SavingsAccount,
    CurrentAccount,
    accounts,
    save_accounts,
    save_transaction,
    find_account,
    load_accounts
)

load_accounts()

root = tk.Tk()
root.title("Bank Management System")
root.geometry("700x600")
root.resizable(True, True)

# ===========================
# Create Frames
# ===========================
home_frame = tk.Frame(root)
create_frame = tk.Frame(root)
deposit_frame = tk.Frame(root)
withdraw_frame = tk.Frame(root)
search_frame = tk.Frame(root)
delete_frame = tk.Frame(root)
balance_frame = tk.Frame(root)
history_frame = tk.Frame(root)

ALL_FRAMES = [
    home_frame, create_frame, deposit_frame, withdraw_frame,
    search_frame, delete_frame, balance_frame, history_frame
]


def show_frame(frame):
    for f in ALL_FRAMES:
        f.pack_forget()
    frame.pack(fill="both", expand=True)


# ===========================
# HOME FRAME
# ===========================
tk.Label(
    home_frame, text="BANK MANAGEMENT SYSTEM", font=("Arial", 22, "bold")
).pack(pady=25)

tk.Label(home_frame, text="Choose an Option", font=("Arial", 12)).pack(pady=5)

tk.Button(
    home_frame, text="Create Account", width=25, height=2,
    command=lambda: show_frame(create_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Deposit Money", width=25, height=2,
    command=lambda: show_frame(deposit_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Withdraw Money", width=25, height=2,
    command=lambda: show_frame(withdraw_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Search Account", width=25, height=2,
    command=lambda: show_frame(search_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Delete Account", width=25, height=2,
    command=lambda: show_frame(delete_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Show Accounts", width=25, height=2,
    command=lambda: show_accounts_gui()
).pack(pady=5)

tk.Button(
    home_frame, text="Total Bank Balance", width=25, height=2,
    command=lambda: (show_frame(balance_frame), refresh_balance_label())
).pack(pady=5)

tk.Button(
    home_frame, text="Transaction History", width=25, height=2,
    command=lambda: show_frame(history_frame)
).pack(pady=5)

tk.Button(
    home_frame, text="Exit", width=25, height=2, bg="red", fg="white",
    command=root.destroy
).pack(pady=20)

# ===========================
# CREATE ACCOUNT FRAME
# ===========================
tk.Label(
    create_frame, text="CREATE ACCOUNT", font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(create_frame, text="Account Number").pack()
account_entry = tk.Entry(create_frame, width=30)
account_entry.pack(pady=5)

tk.Label(create_frame, text="Name").pack()
name_entry = tk.Entry(create_frame, width=30)
name_entry.pack(pady=5)

tk.Label(create_frame, text="Opening Balance").pack()
balance_entry = tk.Entry(create_frame, width=30)
balance_entry.pack(pady=5)

tk.Label(create_frame, text="Account Type").pack()
account_type = tk.StringVar(value="Savings")
tk.OptionMenu(create_frame, account_type, "Savings", "Current").pack(pady=5)


def create_account_gui():
    try:
        account_no = int(account_entry.get())
        name = name_entry.get().strip()
        balance = float(balance_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter a valid account number and balance"
        )
        return

    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return

    if find_account(account_no):
        messagebox.showerror("Error", "Account number already exists")
        return

    if account_type.get() == "Savings":
        account = SavingsAccount(account_no, name, balance)
    else:
        account = CurrentAccount(account_no, name, balance)

    accounts.append(account)
    save_transaction(account.account_no, "Account Created", balance, account.balance)
    save_accounts()

    messagebox.showinfo("Success", "Account Created Successfully")
    account_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    balance_entry.delete(0, tk.END)


tk.Button(
    create_frame, text="Create Account", width=20, command=create_account_gui
).pack(pady=20)

tk.Button(
    create_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()

# ===========================
# DEPOSIT FRAME
# ===========================
tk.Label(
    deposit_frame, text="DEPOSIT MONEY", font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(deposit_frame, text="Account Number").pack()
deposit_account_entry = tk.Entry(deposit_frame, width=30)
deposit_account_entry.pack(pady=5)

tk.Label(deposit_frame, text="Amount").pack()
deposit_amount_entry = tk.Entry(deposit_frame, width=30)
deposit_amount_entry.pack(pady=5)


def deposit_gui():
    try:
        account_no = int(deposit_account_entry.get())
        amount = float(deposit_amount_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter a valid account number and amount"
        )
        return

    account = find_account(account_no)
    if account:
        account.deposit(amount)
        save_transaction(account.account_no, "Deposit", amount, account.balance)
        save_accounts()
        messagebox.showinfo("Success", "Amount Deposited Successfully")
        deposit_amount_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Account Not Found")


tk.Button(
    deposit_frame, text="Deposit", width=20, command=deposit_gui
).pack(pady=20)

tk.Button(
    deposit_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()

# ===========================
# WITHDRAW FRAME
# ===========================
tk.Label(
    withdraw_frame, text="WITHDRAW MONEY", font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(withdraw_frame, text="Account Number").pack()
withdraw_account_entry = tk.Entry(withdraw_frame, width=30)
withdraw_account_entry.pack(pady=5)

tk.Label(withdraw_frame, text="Amount").pack()
withdraw_amount_entry = tk.Entry(withdraw_frame, width=30)
withdraw_amount_entry.pack(pady=5)


def withdraw_gui():
    try:
        account_no = int(withdraw_account_entry.get())
        amount = float(withdraw_amount_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter a valid account number and amount"
        )
        return

    account = find_account(account_no)
    if account:
        if account.balance >= amount:
            account.withdraw(amount)
            save_transaction(account.account_no, "Withdraw", amount, account.balance)
            save_accounts()
            messagebox.showinfo("Success", "Amount Withdrawn Successfully")
            withdraw_amount_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Insufficient Balance")
    else:
        messagebox.showerror("Error", "Account Not Found")


tk.Button(
    withdraw_frame, text="Withdraw", width=20, command=withdraw_gui
).pack(pady=20)

tk.Button(
    withdraw_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()

# ===========================
# SEARCH FRAME
# ===========================
tk.Label(
    search_frame, text="SEARCH ACCOUNT", font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(search_frame, text="Account Number").pack()
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(pady=5)


def search_account_gui():
    try:
        account_no = int(search_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid account number")
        return

    account = find_account(account_no)
    if account:
        messagebox.showinfo(
            "Account Found",
            f"Account No : {account.account_no}\n\n"
            f"Name : {account.name}\n\n"
            f"Type : {account.__class__.__name__}\n\n"
            f"Balance : ₹{account.balance}"
        )
    else:
        messagebox.showerror("Error", "Account Not Found")


tk.Button(
    search_frame, text="Search", width=20, command=search_account_gui
).pack(pady=20)

tk.Button(
    search_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()

# ===========================
# DELETE FRAME
# ===========================
tk.Label(
    delete_frame, text="DELETE ACCOUNT", font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(delete_frame, text="Account Number").pack()
delete_entry = tk.Entry(delete_frame, width=30)
delete_entry.pack(pady=5)


def delete_account_gui():
    try:
        account_no = int(delete_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid account number")
        return

    account = find_account(account_no)
    if account:
        accounts.remove(account)
        save_accounts()
        messagebox.showinfo("Success", "Account Deleted Successfully")
        delete_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Account Not Found")


tk.Button(
    delete_frame, text="Delete Account", width=20, command=delete_account_gui
).pack(pady=20)

tk.Button(
    delete_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()

# ===========================
# TOTAL BALANCE FRAME
# ===========================
tk.Label(
    balance_frame, text="TOTAL BANK BALANCE", font=("Arial", 20, "bold")
).pack(pady=20)

balance_value_label = tk.Label(balance_frame, text="", font=("Arial", 16))
balance_value_label.pack(pady=10)


def refresh_balance_label():
    total = sum(acc.balance for acc in accounts)
    balance_value_label.config(text=f"₹{total}")


tk.Button(
    balance_frame, text="Refresh", width=20, command=refresh_balance_label
).pack(pady=10)

tk.Button(
    balance_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack()


def show_accounts_gui():
    show_window = tk.Toplevel(root)
    show_window.title("All Accounts")
    show_window.geometry("600x400")

    tk.Label(
        show_window, text="ALL ACCOUNTS", font=("Arial", 16, "bold")
    ).pack(pady=10)

    tk.Label(
        show_window,
        text="Account No      Name            Type             Balance",
        font=("Arial", 11, "bold")
    ).pack()

    tk.Label(show_window, text="-" * 64).pack()

    if not accounts:
        tk.Label(show_window, text="No accounts yet.").pack(pady=10)

    for account in accounts:
        info = (
            f"{account.account_no:<15}"
            f"{account.name:<15}"
            f"{account.__class__.__name__:<18}"
            f"₹{account.balance}"
        )
        tk.Label(
            show_window, text=info, font=("Courier New", 11)
        ).pack(anchor="w", padx=20)


# ===========================
# TRANSACTION HISTORY FRAME
# ===========================
TRANSACTIONS_FILE = "transactions.json"
 
tk.Label(
    history_frame, text="TRANSACTION HISTORY", font=("Arial", 20, "bold")
).pack(pady=15)
 
history_filter_row = tk.Frame(history_frame)
history_filter_row.pack(pady=5)
 
tk.Label(history_filter_row, text="Account No:").pack(side="left", padx=5)
history_filter_entry = tk.Entry(history_filter_row, width=15)
history_filter_entry.pack(side="left", padx=5)
 
history_tree_frame = tk.Frame(history_frame)
history_tree_frame.pack(pady=10, padx=20, fill="both", expand=True)
 
history_columns = ("account_no", "type", "amount", "balance", "date", "time")
history_tree = ttk.Treeview(
    history_tree_frame, columns=history_columns, show="headings", height=15
)
 
history_tree.heading("account_no", text="Account No")
history_tree.heading("type", text="Type")
history_tree.heading("amount", text="Amount")
history_tree.heading("balance", text="Balance")
history_tree.heading("date", text="Date")
history_tree.heading("time", text="Time")
 
history_tree.column("account_no", width=90, anchor="center")
history_tree.column("type", width=130, anchor="center")
history_tree.column("amount", width=100, anchor="e")
history_tree.column("balance", width=110, anchor="e")
history_tree.column("date", width=90, anchor="center")
history_tree.column("time", width=100, anchor="center")
 
history_scrollbar = ttk.Scrollbar(
    history_tree_frame, orient="vertical", command=history_tree.yview
)
history_tree.configure(yscrollcommand=history_scrollbar.set)
 
history_tree.pack(side="left", fill="both", expand=True)
history_scrollbar.pack(side="right", fill="y")
 
 
def load_transactions():
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
 
 
def refresh_history_view():
    for row in history_tree.get_children():
        history_tree.delete(row)
 
    filter_text = history_filter_entry.get().strip()
    account_no = None
    if filter_text:
        try:
            account_no = int(filter_text)
        except ValueError:
            messagebox.showerror("Error", "Account number must be a number")
            return
 
    transactions = load_transactions()
 
    if account_no is not None:
        transactions = [t for t in transactions if t.get("account_no") == account_no]
 
    if not transactions:
        history_tree.insert(
            "", "end", values=("", "No transactions found", "", "", "", "")
        )
        return
 
    # newest first
    for t in reversed(transactions):
        history_tree.insert(
            "", "end",
            values=(
                t.get("account_no", ""),
                t.get("type", ""),
                f"₹{t.get('amount', '')}",
                f"₹{t.get('balance', '')}",
                t.get("date", ""),
                t.get("time", "")
            )
        )
 
 
def show_all_history():
    history_filter_entry.delete(0, tk.END)
    refresh_history_view()
 
 
def open_history_frame():
    history_filter_entry.delete(0, tk.END)
    refresh_history_view()
    show_frame(history_frame)
 
 
tk.Button(
    history_filter_row, text="Filter", width=10, command=refresh_history_view
).pack(side="left", padx=5)
 
tk.Button(
    history_filter_row, text="Show All", width=10, command=show_all_history
).pack(side="left", padx=5)
 
tk.Button(
    history_frame, text="Back", width=20, command=lambda: show_frame(home_frame)
).pack(pady=15)
 
# ===========================
# Show Home First & Start the App
# ===========================
show_frame(home_frame)
root.mainloop()