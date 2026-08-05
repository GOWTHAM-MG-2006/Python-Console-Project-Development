from dataclasses import dataclass, field
from collections import defaultdict


@dataclass(frozen=True)
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


class NoTransactionHistoryFound(Exception):
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


def reverse_last_transaction(acc_id):
    customer_acc = get_account(acc_id)
    transaction_history = customer_acc.transactions
    if len(transaction_history) == 0:
        raise NoTransactionHistoryFound
    last_transaction = transaction_history[-1]
    if last_transaction.operation == "withdraw":
        customer_acc.balance += last_transaction.amount
    else:
        if customer_acc.balance < last_transaction.amount:
            raise InsufficientFundsError
        customer_acc.balance -= last_transaction.amount
    transaction_history.pop()
    print(
        f"The Last Transaction {last_transaction.operation} of Amount {last_transaction.amount} Has Been Reversed Successfully"
    )
    return customer_acc.balance


def transfer(from_id, to_id, amount):
    from_acc = get_account(from_id)
    to_acc = get_account(to_id)
    amountcheck(amount)
    if from_acc.balance < amount:
        raise InsufficientFundsError
    source_transaction_history = from_acc.transactions.copy()
    source_balance = from_acc.balance
    target_transaction_history = to_acc.transactions.copy()
    target_balance = to_acc.balance
    try:
        withdraw(from_id, amount)
        deposit(to_id, amount)
    except:
        from_acc.balance = source_balance
        from_acc.transactions = source_transaction_history
        to_acc.balance = target_balance
        to_acc.transactions = target_transaction_history
        raise


def deposit(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0:
        customer_acc.balance += amount
        current_Transaction = Transaction("deposit", amount)
        customer_acc.transactions.append(current_Transaction)
        return customer_acc.balance
    else:
        amountcheck(amount)
        return customer_acc.balance


def withdraw(acc_id, amount):
    customer_acc = get_account(acc_id)
    if amount > 0 and amount <= customer_acc.balance:
        customer_acc.balance -= amount
        current_Transaction = Transaction("withdraw", amount)
        customer_acc.transactions.append(current_Transaction)
        return customer_acc.balance
    else:
        if amount > customer_acc.balance:
            raise InsufficientFundsError
        else:
            amountcheck(amount)
            return customer_acc.balance


def checkbalance(acc_id):
    customer_acc = get_account(acc_id)
    return customer_acc.balance


def close_account(acc_id):
    customer_account = get_account(acc_id)
    customer_index[customer_account.customer_name].remove(acc_id)
    if not customer_index[customer_account.customer_name]:
        del customer_index[customer_account.customer_name]
    del accounts[acc_id]
    print("Account Closed Successfully")


while True:
    print("+------------------ JJ-BANK ------------------+")
    print("|         1. CREATE ACCOUNT                   |")
    print("|         2. DEPOSIT                          |")
    print("|         3. WITHDRAW                         |")
    print("|         4. CHECK BALANCE                    |")
    print("|         5. TRANSFER MONEY                   |")
    print("|         6. REVERSE LAST TRANSACTION         |")
    print("|         7. FIND ACCOUNTS BY CUSTOMER NAME   |")
    print("|         8. CLOSE ACCOUNT                    |")
    print("|         9. EXIT                             |")
    print("+---------------------------------------------+")
    try:
        print("Enter Your Choice:")
        ch = int(input())
        match ch:
            case 1:  # Create
                print("Enter Customer Name:")
                name = input()
                new_id = create_account(name)
                print("Account ID:", new_id)
            case 2:  # Deposit
                print("Enter Account ID:")
                user_id = int(input())
                print("Enter Amount To Be Deposited:")
                amount = float(input())
                balance = deposit(user_id, amount)
                print("Available Balance:", balance)
            case 3:  # Withdraw
                print("Enter Account ID:")
                user_id = int(input())
                print("Enter Amount To Be Withdrawn:")
                amount = float(input())
                balance = withdraw(user_id, amount)
                print("Available Balance:", balance)
            case 4:  # Check Balance
                print("Enter Account ID:")
                user_id = int(input())
                balance = checkbalance(user_id)
                print("Available Balance:", balance)
            case 5:  # TRANSFER MONEY
                print("Enter Your Account ID:")
                from_id = int(input())
                print("Enter Receiver Account ID:")
                to_id = int(input())
                print("Enter Amount To Be Transferred:")
                amount = float(input())
                transfer(from_id, to_id, amount)
                print("Amount Transferred Successfully")
            case 6:  # REVERSE LAST TRANSACTION
                print("Enter Account ID:")
                customer_id = int(input())
                updated_balance = reverse_last_transaction(customer_id)
                print(
                    f"Reversal of Last Transaction Successful And The Updated Balance Is: {updated_balance}"
                )
            case 7:  # FIND ACCOUNTS BY CUSTOMER NAME
                print("Enter The Name of The Customer:")
                customer_name = input()
                account_list = find_accounts_by_customer(customer_name)
                print(f"Accounts Held By The Customer Named {customer_name} Is:")
                print(*account_list)
            case 8:  # Close Account
                print("Enter Account ID To Be Deleted:")
                user_id = int(input())
                close_account(user_id)
            case 9:  # Exit
                print("Thanks For Visiting JJ-Bank")
                break
            case _:
                print("Invalid Choice")
    except AccountNotFoundError as e:
        print("Account Not Found")
    except InsufficientFundsError as e:
        print("Insufficient Funds")
    except ValueError as e:
        print("Enter Valid Input")
    except NegativeAmount as e:
        print("Amount Cannot Be Negative")
    except ZeroAmount as e:
        print("Amount Cannot Be Zero")
    except CustomerNotExist as e:
        print("Customer Does Not Exist")
    except NoTransactionHistoryFound as e:
        print("No Transaction History Found")
