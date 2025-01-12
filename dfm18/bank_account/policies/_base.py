from typing import Protocol, runtime_checkable

from abc import abstractmethod

from enum import Flag, auto

from .._base import BankAccount


class PolicyOperation(Flag):
    DEPOSIT = auto()
    WITHDRAW = auto()


@runtime_checkable
class Policy(Protocol):
    @abstractmethod
    def apply(self, account: BankAccount, amount: float): ...

    @abstractmethod
    def supports(self, operation: PolicyOperation) -> bool: ...
