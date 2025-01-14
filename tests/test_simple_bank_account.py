import unittest

from unittest.mock import patch, Mock

import os

from dfm18.bank_account._simple import SimpleBankAccount

from dfm18.bank_account.policies import Policy


class TestSimpleBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = SimpleBankAccount(balance=1000, log_file="transaction.log")

    def tearDown(self):
        for handler in self.account._logger.handlers:
            handler.close()

        if self.account.log_file is not None and os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

    @patch("dfm18.bank_account.policies.Policy")
    def test_initialization_with_policies(self, mock_policy: Mock):
        mock_policy_1 = Mock(spec=Policy)
        mock_policy_2 = Mock(spec=Policy)

        mock_policy_1.apply.return_value = None
        mock_policy_1.supports.return_value = True
        mock_policy_2.apply.return_value = None
        mock_policy_2.supports.return_value = False

        policies = [mock_policy_1, mock_policy_2]

        self.account = SimpleBankAccount(balance=1000, policies=policies)

        self.assertEqual(len(self.account.policies), 2)
        self.assertIn(mock_policy_1, self.account.policies)
        self.assertIn(mock_policy_2, self.account.policies)
        self.assertEqual(self.account.policies, policies)

        mock_policy_1.apply.assert_not_called()
        mock_policy_1.supports.assert_not_called()
        mock_policy_2.apply.assert_not_called()
        mock_policy_2.supports.assert_not_called()

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500)

    def test_deposit_on_negative_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_deposit_on_zero_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    @patch("dfm18.bank_account.policies.Policy")
    def test_deposit_on_policy_violation_raises_exception(self, mock_policy: Mock):
        mock_policy.apply.side_effect = Exception("Policy Restriction")
        mock_policy.supports.return_value = True

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        with self.assertRaises(Exception) as context:
            self.account.deposit(100)

        self.assertEqual(str(context.exception), "Policy Restriction")

    @patch("dfm18.bank_account.policies.Policy")
    def test_deposit_allowed_by_policy(self, mock_policy: Mock):
        mock_policy.apply.return_value = None
        mock_policy.supports.return_value = True

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        amount = 100

        try:
            self.account.deposit(amount)
        except Exception as e:
            self.fail(f"Unexepected exception: {str(e)}")

        mock_policy.apply.assert_called_once_with(self.account, amount)
        mock_policy.supports.assert_called_once()

    @patch("dfm18.bank_account.policies.Policy")
    def test_deposit_allowed_due_to_missing_policies_for_operation(
        self, mock_policy: Mock
    ):
        mock_policy.apply.return_value = None
        mock_policy.supports.return_value = False

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        amount = 100

        try:
            self.account.deposit(amount)
        except Exception as e:
            self.fail(f"Unexepected exception: {str(e)}")

        mock_policy.apply.assert_not_called()
        mock_policy.supports.assert_called_once()

    def test_withdraw(self):
        new_balance = self.account.withdraw(200)
        self.assertEqual(new_balance, 800)

    def test_withdraw_on_negative_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100)

    def test_withdraw_on_zero_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    @patch("dfm18.bank_account.policies.Policy")
    def test_withdraw_on_policy_violation_raises_exception(self, mock_policy: Mock):
        mock_policy.apply.side_effect = Exception("Policy Restriction")
        mock_policy.supports.return_value = True

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        with self.assertRaises(Exception) as context:
            self.account.withdraw(100)

        self.assertEqual(str(context.exception), "Policy Restriction")

    @patch("dfm18.bank_account.policies.Policy")
    def test_withdraw_allowed_by_policy(self, mock_policy: Mock):
        mock_policy.apply.return_value = None
        mock_policy.supports.return_value = True

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        amount = 100

        try:
            self.account.withdraw(amount)
        except Exception as e:
            self.fail(f"Unexepected exception: {str(e)}")

        mock_policy.apply.assert_called_once_with(self.account, amount)
        mock_policy.supports.assert_called_once()

    @patch("dfm18.bank_account.policies.Policy")
    def test_withdraw_allowed_due_to_missing_policies_for_operation(
        self, mock_policy: Mock
    ):
        mock_policy.apply.return_value = None
        mock_policy.supports.return_value = False

        self.account = SimpleBankAccount(balance=1000, policies=[mock_policy])

        amount = 100

        try:
            self.account.withdraw(amount)
        except Exception as e:
            self.fail(f"Unexepected exception: {str(e)}")

        mock_policy.apply.assert_not_called()
        mock_policy.supports.assert_called_once()

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
