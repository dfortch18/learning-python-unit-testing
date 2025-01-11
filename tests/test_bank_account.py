import unittest

import os

from dfm18.bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(balance=1000, log_file="transaction.log")

    def tearDown(self):
        for handler in self.account._logger.handlers:
            handler.close()

        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

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

    def test_logger(self):
        with self.assertLogs(self.account._logger) as log_file:
            self.account.deposit(1000)
            self.assertIn("Deposited 1000.00. New balance: 2000.00", log_file.output[0])
            self.account.withdraw(50)
            self.assertIn("Withdrew 50.00. New balance: 1950.00", log_file.output[1])
