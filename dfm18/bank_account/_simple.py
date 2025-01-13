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
        """
        Simple Bank Account.

        Args:
            balance (float, optional): Initial account balance. Defaults to 0.
            log_file (Optional[str], optional): Optional log file for logging transactions. Defaults to None.
            policies (Optional[List[Policy]], optional): List of policies to enforce on operations. Defaults to None.

        Example:
            >>> account = SimpleBankAccount(balance=100)
            >>> account.balance
            100
            >>> account.deposit(50)
            150
            >>> account.withdraw(30)
            120
        """
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
        """
        Deposit an amount into the account and return the new balance.

        Args:
            amount (float): The amount to deposit.

        Returns:
            float: The updated balance.

        Example:
            >>> account = SimpleBankAccount()
            >>> account.deposit(50)
            50
            >>> account.deposit(25)
            75
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self._apply_policies(amount, PolicyOperation.DEPOSIT)

        self._balance += amount
        self._logger.info("Deposited %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    def withdraw(self, amount: float) -> float:
        """
        Withdraw an amount from the account and return the new balance.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            float: The updated balance.

        Example:
            >>> account = SimpleBankAccount(balance=100)
            >>> account.withdraw(40)
            60
            >>> account.withdraw(20)
            40
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self._apply_policies(amount, PolicyOperation.WITHDRAW)

        self._balance -= amount
        self._logger.info("Withdrew %.2f. New balance: %.2f", amount, self.balance)
        return self._balance

    @property
    def balance(self) -> float:
        """
        Retrieve the current balance of the account.

        Returns:
            float: The current balance.

        Example:
            >>> account = SimpleBankAccount(balance=200)
            >>> account.balance
            200
        """
        return self._balance
