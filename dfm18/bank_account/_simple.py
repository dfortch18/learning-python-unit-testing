from typing import Optional, List

from ._base import BankAccount

from .policies import Policy, PolicyOperation

import logging


class SimpleBankAccount(BankAccount):
    def __init__(
        self,
        balance: float = 0,
        log_file: Optional[str] = None,
        policies: Optional[List[Policy]] = None,
    ):
        self._balance = balance
        self.log_file = log_file
        self.policies = policies or []
        self._setup_logger()

    def _setup_logger(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        if self.log_file is not None:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(message)s", datefmt="%b %d, %Y %H:%M:%S"
            )
            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)

    def _apply_policies(self, amount, operation: PolicyOperation):
        for policy in self.policies:
            if policy.supports(operation):
                policy.apply(self, amount)

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        self._apply_policies(amount, PolicyOperation.DEPOSIT)

        self._balance += amount
        self._logger.info("Deposited %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self._apply_policies(amount, PolicyOperation.WITHDRAW)

        self._balance -= amount
        self._logger.info("Withdrew %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance
