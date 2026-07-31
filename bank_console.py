from dataclasses import dataclass


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float


accounts: dict[int, Account] = {}


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass
