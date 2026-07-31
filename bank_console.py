from dataclasses import dataclass
from email.policy import default


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float


acc_id = 101
accounts: dict[int, Account] = {}


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


def amountcheck(amount):
    if amount < 0:
        print("Amount Cannot Be Negative")
    elif amount == 0:
        print("Amount Cannot Be Zero")


def create_account(customer_name):
    global acc_id
    accounts[acc_id] = Account(acc_id, customer_name, 0.00)
    cur_id = acc_id
    acc_id += 1
    print("Account Created Successfully")
    return cur_id


def get_account(acc_id):
    if acc_id in accounts:
        return accounts[acc_id]
    else:
        raise AccountNotFoundError


def deposit(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0:
        customer_acc.balance += amount
        return customer_acc.balance
    else:
        amountcheck(amount)
        return customer_acc.balance


def withdraw(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0 and amount <= customer_acc.balance:
        customer_acc.balance -= amount
        return customer_acc.balance
    else:
        if amount > customer_acc.balance:
            raise InsufficientFundsError
        else:
            amountcheck(amount)
            return customer_acc.balance

def checkbalance(acc_id):
    customer_acc=get_account(acc_id)
    return customer_acc.balance

def close_account(acc_id):
    customer_acc=get_account(acc_id)
    del accounts[acc_id]
    print("Account Closed Successfully")

while True:
    print("+------------------ JJ-BANK ------------------+")
    print("|         1. CREATE ACCOUNT                   |")
    print("|         2. DEPOSIT                          |")
    print("|         3. WITHDRAW                         |")
    print("|         4. CHECK BALANCE                    |")
    print("|         5. CLOSE ACCOUNT                    |")
    print("|         6. EXIT                             |")
    print("+---------------------------------------------+")
    print("Enter Your Choice:")
    ch=int(input())
    try:
        match ch:
            case 1: #Create
                print("Enter Customer Name:")
                name=input()
                acc_id=create_account(name)
                print("Account ID:",acc_id)
            case 2: #Deposit
                print("Enter Account ID:")
                acc_id=int(input())
                print("Enter Amount To Be Deposited:")
                amount=int(input())
                balance=deposit(acc_id,amount)
                print("Available Balance:",balance)
            case 3: #Withdraw
                print("Enter Account ID:")
                acc_id=int(input())
                print("Enter Amount To Be Withdrawn:")
                amount=int(input())
                balance=withdraw(acc_id,amount)
                print("Available Balance:",balance)
            case 4: #Check Balance
                print("Enter Account ID:")
                acc_id=int(input())
                balance=checkbalance(acc_id)
                print("Available Balance:",balance)
            case 5: #Close Account
                print("Enter Account ID To Be Deleted:")
                acc_id=int(input())
                close_account(acc_id)
            case 6: #Exit
                print("Thanks For Visiting JJ-Bank")
                break
            case _:
                print("Invalid Choice")
