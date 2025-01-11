from typing import Protocol, runtime_checkable


@runtime_checkable
class BankAccount(Protocol):
    def deposit(self, amount: float) -> float: ...

    def withdraw(self, amount: float) -> float: ...

    @property
    def balance(self) -> float: ...
