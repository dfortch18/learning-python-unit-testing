from typing import Protocol, runtime_checkable

from abc import abstractmethod


@runtime_checkable
class BankAccount(Protocol):
    @abstractmethod
    def deposit(self, amount: float) -> float:
        """
        Deposits a specified amount into the account and returns the updated balance.

        Args:
            amount (float): The amount to deposit. Must be greater than zero.

        Returns:
            float: The updated account balance.
        """
        ...

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """
        Withdraws a specified amount from the account and returns the updated balance.

        Args:
            amount (float): The amount to withdraw. Must be greater than zero.

        Returns:
            float: The updated account balance.
        """
        ...

    @abstractmethod
    def get_balance(self) -> float:
        """
        Retrieves the current account balance.

        Returns:
            float: The current account balance.
        """
        ...

    @property
    def balance(self) -> float:
        """
        Retrieves the current balance of the account.

        Returns:
            float: The current balance.
        """
        return self.get_balance()
