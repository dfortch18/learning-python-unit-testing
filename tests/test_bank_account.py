import unittest

from dfm18.bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(balance=1000)

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500)

    def test_withdraw(self):
        new_balance = self.account.withdraw(200)
        self.assertEqual(new_balance, 800)

    def test_balance_property(self):
        self.assertEqual(self.account.balance, 1000)
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, 500)
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 600)
