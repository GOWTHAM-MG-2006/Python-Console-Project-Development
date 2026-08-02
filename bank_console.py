from dataclasses import dataclass,field
from collections import defaultdict

@dataclass
class Transaction:
    operation: str
    amount: float
@dataclass
class Account:
    id: int
    customer_name: str
    balance: float
    transactions: list[Transaction] = field(default_factory=list)

acc_id = 101
customer_index = defaultdict(list)
accounts: dict[int, Account] = {}


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass

class NegativeAmount(Exception):
    pass

class ZeroAmount(Exception):
    pass

class CustomerNotExist(Exception):
    pass

def amountcheck(amount):
    if amount < 0:
        raise NegativeAmount
    elif amount == 0:
        raise ZeroAmount


def create_account(customer_name):
    global acc_id
    accounts[acc_id] = Account(acc_id, customer_name, 0.00)
    cur_id = acc_id
    customer_index[customer_name].append(cur_id)
    acc_id += 1
    print("Account Created Successfully")
    return cur_id


def get_account(acc_id):
    if acc_id in accounts:
        return accounts[acc_id]
    else:
        raise AccountNotFoundError

def find_accounts_by_customer(name):
    if name in customer_index:
        return customer_index[name]
    else:
        raise CustomerNotExist


def deposit(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0:
        customer_acc.balance += amount
        current_Transaction=Transaction("deposit",amount)
        customer_acc.transactions.append(current_Transaction)
        return customer_acc.balance
    else:
        amountcheck(amount)
        return customer_acc.balance


def withdraw(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0 and amount <= customer_acc.balance:
        customer_acc.balance -= amount
        current_Transaction=Transaction("withdraw",amount)
        customer_acc.transactions.append(current_Transaction)
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
    get_account(acc_id)
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
    try:
        print("Enter Your Choice:")
        ch=int(input())
        match ch:
            case 1: #Create
                print("Enter Customer Name:")
                name=input()
                new_id=create_account(name)
                print("Account ID:",new_id)
            case 2: #Deposit
                print("Enter Account ID:")
                user_id=int(input())
                print("Enter Amount To Be Deposited:")
                amount=float(input())
                balance=deposit(user_id,amount)
                print("Available Balance:",balance)
            case 3: #Withdraw
                print("Enter Account ID:")
                user_id=int(input())
                print("Enter Amount To Be Withdrawn:")
                amount=float(input())
                balance=withdraw(user_id,amount)
                print("Available Balance:",balance)
            case 4: #Check Balance
                print("Enter Account ID:")
                user_id=int(input())
                balance=checkbalance(user_id)
                print("Available Balance:",balance)
            case 5: #Close Account
                print("Enter Account ID To Be Deleted:")
                user_id=int(input())
                close_account(user_id)
            case 6: #Exit
                print("Thanks For Visiting JJ-Bank")
                break
            case _:
                print("Invalid Choice")
    except AccountNotFoundError:
        print("Account Not Found")
    except InsufficientFundsError:
        print("Insufficient Funds")
    except ValueError:
        print("Enter Valid Input")
    except NegativeAmount:
        print("Amount Cannot Be Negative")
    except ZeroAmount:
        print("Amount Cannot Be Zero")