from typing import Optional

from ._base import BankAccount

import logging


class SimpleBankAccount(BankAccount):
    def __init__(self, balance: float = 0, log_file: Optional[str] = None):
        self._balance = balance
        self.log_file = log_file
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

    def deposit(self, amount: float) -> float:
        if amount > 0:
            self._balance += amount
            self._logger.info("Deposited %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount > 0:
            self._balance -= amount
            self._logger.info("Withdrew %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance
