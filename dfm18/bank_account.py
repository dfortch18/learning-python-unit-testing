class BankAccount:
    def __init__(self, balance: float = 0):
        self._balance = balance

    def deposit(self, amount: float) -> float:
        if amount > 0:
            self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount > 0:
            self._balance -= amount
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance
