from typing import Protocol, runtime_checkable


@runtime_checkable
class BankAccount(Protocol):
    def deposit(self, amount: float) -> float:
        """
        Deposit an amount into the account and returns the new balance.

        Args:
            amount (float): The amount to deposit

        Returns:
            float: The new balance
        """
        ...

    def withdraw(self, amount: float) -> float:
        """
        Withdraw an amount from the account and return the new balance.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            float: The new balance.
        """
        ...

    @property
    def balance(self) -> float:
        """
        Retrieve the current balance of the account.

        Returns:
            float: The current balance.
        """
        ...
