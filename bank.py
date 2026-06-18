import json
from datetime import datetime
class Account :
    def __init__ (self, account_no , name, balance):
        self.account_type = "Account"
        self.account_no = account_no
        self.name = name 
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount > 0 :
            self.balance += amount

            self.history.append(
                f"Deposited ₹{amount}"
            )

    def withdraw(self, amount):
        if amount <=self.balance:
            self.balance -= amount

            self.history.append(
            f"Withdrawn ₹{amount}"
            )

        else:
            print("Insufficient Balance")

    def display(self):
        print("Account Type:", self.__class__.__name__)
        print("Account No:", self.account_no)
        print("Name:",self.name)
        print("Balance:",self.balance)

class SavingsAccount(Account):
    def __init__(self, account_no, name, balance):
        super().__init__(account_no, name, balance)
    
class CurrentAccount(Account):
    def __init__(self, account_no, name, balance):
        super().__init__(account_no, name, balance) 

accounts=[]
def create_account():
    print("1. Savings Account")
    print("2. Current Account")

    account_type =int(input("Select Account Type:"))

    account_no = int (input("Enter Account Number:"))
    if find_account(account_no):
        print("Account Number Already Exists")
        return 
    
    name = input("Enter Name:")
    balance = float(input("Enter Intial Balance:"))

    if account_type == 1:
        account = SavingsAccount(account_no, name , balance)
    
    elif account_type ==2:
        account = CurrentAccount(account_no , name , balance)

    else: 
        print("Invalid Account Type")
        return 

    # account = Account(account_no , name , balance)

    accounts.append(account)
    save_transaction(
    account.account_no,
    "Account Created",
    balance,
    account.balance
)

    save_accounts()

    account.history.append(
        "Account Created"
    )

    print("Account created successfully")

def delete_account():
    account_no = int(input("Enter Account Number:"))

    account = find_account(account_no)

    if account :
        accounts.remove(account)
        save_accounts()

        print("Account Deleted Successfully")

    else:
        print("Account Not Found")

def total_bank_balance():
    total = 0 
    for account in accounts:
        total += account.balance

    print("Total Bank Balance:",total)

def save_accounts():
    data=[]
    for account in accounts:
        data.append({
            "account_type": account.__class__.__name__,
            "account_no": account.account_no,
            "name": account.name,
            "balance": account.balance
    })

    with open ("accounts.json", "w") as file:
        json.dump(data, file, indent=4) 

def show_accounts():

    if len(accounts)==0:
        print("No Accounts Found")
        return
    
    print("\n===== ALL ACCOUNTS =====")

    for account in accounts:
        account.display()
        print("-" * 30)

def find_account(account_no):

    for account in accounts:
        if account.account_no == account_no:
            return account
    
    return None

def deposit_money():
    account_no = int(input("Enter Account Number:"))
    account = find_account(account_no)

    if account:
        amount = float(input("Enter Amount:"))
        account.deposit(amount)
        save_transaction(
            account.account_no,
            "Deposit",
            amount,
            account.balance
        )
        save_accounts()
        print("Amount Deposit Successfully")
    else: 
        print ("Amount Not Found")

def check_balance():
    account_no = int(input("Enter Account Number:"))
    account = find_account (account_no)

    if account:
        print ("Current Balance:", account.balance)

    else:
        print("Account Not Found")

def withdraw_money():
    account_no = int(input("Enter Account Number:"))
    account = find_account(account_no)
   
    if account:
        amount = float(input("Enter Amount :"))
        account.withdraw(amount)
        save_transaction(
            account.account_no,
            "Withdraw",
            amount,
            account.balance
            )
        save_accounts()

    else:
        print("Account Not Found")

def show_history():
    account_no = int(input("Enter Account Number:"))

    account = find_account(account_no)

    if account: 
        print("/n Transaction History")

        for transaction in account.history:
            print(transaction)
        
    else:
        print("Account Not Found")

def load_accounts():

    try:

        with open ("accounts.json", "r")as file:

            data= json.load(file)

        for item in data:
            account_type = item.get("account_type", "Account")


            if account_type == "Savings Account":
                account = SavingsAccount
                (
                    item["account_no"],
                    item["name"],
                    item["balance"]
                )
        
            elif account_type == "Current Account":
                account = CurrentAccount (
                    item["account_no"],
                    item["name"],
                    item["balance"]
                )
        
            else:
                account = Account(
                    item["account_no"],
                    item["name"],
                    item["balance"]
                )

                accounts.append(account)
        
    except FileNotFoundError:

        print("NO Previous Data Found")
    
    if __name__ == "__main__":
        load_accounts()

        while True:

            print(" =====Bank Management System=====")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Show Accounts")
            print("6. Delete Account")
            print("7. Total Bank Balance")
            print("8. Show History")
            print("9. Exit")
    

            choice = int(input("Enter choice:"))
            if choice == 1:
                create_account()
    
            elif choice ==2:
                deposit_money()

            elif choice ==3:
                withdraw_money()
        
            elif choice ==4:
                check_balance()

            elif choice ==5:
                show_accounts()

            elif choice ==6:
                delete_account()
        
            elif choice == 7:
                total_bank_balance()

            elif choice == 8:
                show_history()

            elif choice ==9:
                print("Thank You")
                break

            else:
                print("Invalid choice")

def save_accounts():
    data=[]
    for account in accounts:
        data.append({
            "account_type": account.__class__.__name__,
            "account_no": account.account_no,
            "name": account.name,
            "balance": account.balance
        })

    with open ("accounts.json", "w") as file:
        json.dump(data, file, indent=4) 

def save_transaction(account_no, transaction_type, amount, balance):

    transaction = {
        "account_no": account_no,
        "type": transaction_type,
        "amount": amount,
        "balance": balance,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "time": datetime.now().strftime("%I:%M:%S %p")
    }

    try:
        with open("transactions.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        data = []

    data.append(transaction)

    with open("transactions.json", "w") as file:
        json.dump(data, file, indent=4)



