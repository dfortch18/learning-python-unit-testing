import unittest

from unittest.mock import patch, Mock

from datetime import datetime

from dfm18.bank_account.policies._base import PolicyOperation

from dfm18.bank_account.policies._withdrawal_time_restriction import (
    WithdrawalTimeRestrictionPolicy,
    WithdrawalTimeRestrictionError,
)


class TestWithdrawalTimeRestrictionPolicy(unittest.TestCase):
    def test_initialization_with_valid_hours(self):
        policy = WithdrawalTimeRestrictionPolicy(8, 17)
        self.assertEqual(policy.start_hour, 8)
        self.assertEqual(policy.end_hour, 17)

    def test_initialization_with_invalid_hour_raises_exception(self):
        with self.assertRaises(ValueError):
            WithdrawalTimeRestrictionPolicy(26, 0)
        with self.assertRaises(ValueError):
            WithdrawalTimeRestrictionPolicy(-1, 0)
        with self.assertRaises(ValueError):
            WithdrawalTimeRestrictionPolicy(0, 34)
        with self.assertRaises(ValueError):
            WithdrawalTimeRestrictionPolicy(0, -1)

    @patch("dfm18.bank_account._base.BankAccount")
    @patch("dfm18.bank_account.policies._withdrawal_time_restriction.datetime")
    def test_apply_inside_allowed_hours(self, mock_datetime: Mock, mock_account: Mock):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0, 0)
        policy = WithdrawalTimeRestrictionPolicy(8, 17)

        try:
            policy.apply(mock_account, 100)
        except WithdrawalTimeRestrictionError:
            self.fail()

    @patch("dfm18.bank_account._base.BankAccount")
    @patch("dfm18.bank_account.policies._withdrawal_time_restriction.datetime")
    def test_apply_outside_allowed_hours_raises_exception(
        self, mock_datetime: Mock, mock_account: Mock
    ):
        mock_datetime.now.side_effect = [
            datetime(2024, 1, 1, 18, 0, 0, 0),
            datetime(2024, 1, 1, 7, 0, 0, 0),
        ]
        policy = WithdrawalTimeRestrictionPolicy(8, 17)

        with self.assertRaises(WithdrawalTimeRestrictionError):
            policy.apply(mock_account, 100)

        with self.assertRaises(WithdrawalTimeRestrictionError):
            policy.apply(mock_account, 100)

    def test_supported_operations(self):
        policy = WithdrawalTimeRestrictionPolicy(8, 17)

        self.assertTrue(policy.supports(policy.supported_operations))
        self.assertFalse(policy.supports(PolicyOperation.DEPOSIT))
