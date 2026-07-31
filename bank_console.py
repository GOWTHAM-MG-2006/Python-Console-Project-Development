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