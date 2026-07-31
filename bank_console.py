from dataclasses import dataclass


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
