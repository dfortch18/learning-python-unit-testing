from ._base import Policy, PolicyOperation

from .._base import BankAccount

from ..exceptions import WithdrawalTimeRestrictionError

from datetime import datetime


class WithdrawalTimeRestrictionPolicy(Policy):
    def __init__(self, start_hour: int, end_hour: int):
        if not (0 <= start_hour <= 24) or not (0 <= end_hour <= 24):
            raise ValueError("Start hour and end hour must be a valid hour")
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.supported_operations = PolicyOperation.WITHDRAW

    def apply(self, account: BankAccount, amount: float):
        now = datetime.now()

        if not (self.start_hour <= now.hour <= self.end_hour):
            raise WithdrawalTimeRestrictionError(
                f"Withdrawals are only allowed between {self.start_hour} and {self.end_hour} hours."
            )

    def supports(self, operation: PolicyOperation) -> bool:
        return bool(self.supported_operations & operation)
