class InsufficientBalanceError(Exception):
    """exception for insufficient balance."""
    pass

class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self,amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive ")
        self.balance += amount
        print(f"{amount}rs deposited successully ")

    def withdraw(self,amount):
        if amount <=0:
            raise ValueError("Withdrawl amount must be positive ")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance ")
        self.balance -= amount
        print(f"{amount}rs withdraw successfully ")

    def check_balance(self):
        print(f"Current balnce : {self.balance}rs")


#---Main Program---#

account = BankAccount()

while True:
    print("\n choose one option ")
    print("1. Deposit ")
    print("2. Withdraw ")
    print("3. Balance Inquiry ")
    print("4. Exit ")

    try:
        ch = int(input("Enter your choice : "))
        if ch == 1:
            amount = float(input("enter deposit amount : "))
            account.deposit(amount)

        elif ch == 2:
            amount = float(input("Enter withdrawl amount : "))
            account.withdraw(amount)

        elif ch == 3:
            account.check_balance()

        elif ch == 4:
            print("Progarm Executed ")
            break

        else:
            print("Enter a valid choice ")

    except ValueError as e:
        print("Value Error : ",e)

    except InsufficientBalanceError as e:
        print("Transaction not completed : ",e)
