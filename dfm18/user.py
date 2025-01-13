from typing import List

from .bank_account import BankAccount

from email_validator import validate_email, EmailNotValidError


class User:
    def __init__(self, name: str, email: str):
        self._validate_email(email)

        self.name = name
        self.email = email
        self.accounts: List[BankAccount] = []

    def _validate_email(self, email: str):
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")

    def add_account(self, account: BankAccount):
        self.accounts.append(account)

    def get_total_balance(self) -> float:
        return sum(account.get_balance() for account in self.accounts)
