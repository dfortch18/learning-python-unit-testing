import unittest

from unittest.mock import patch, Mock

from faker import Faker

from email_validator import EmailNotValidError

from dfm18.user import User

from dfm18.bank_account import BankAccount


class TestUser(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()

    @patch("dfm18.user.validate_email")
    def test_initialization(self, mock_validate_email: Mock):
        name_generated = self.faker.name()
        email_generated = self.faker.email()

        mock_validate_email.return_value = {"email": email_generated}

        user = User(name=name_generated, email=email_generated)

        self.assertEqual(user.name, name_generated)
        self.assertEqual(user.email, email_generated)
        mock_validate_email.assert_called_once_with(
            email_generated, check_deliverability=False
        )

    @patch("dfm18.user.validate_email")
    def test_initialization_on_invalid_email_raises_exception(
        self, mock_validate_email: Mock
    ):
        mock_validate_email.side_effect = EmailNotValidError("Invalid email format")

        name_generated = self.faker.name()
        invalid_email = "invalid-email"

        with self.assertRaises(ValueError) as context:
            User(name=name_generated, email=invalid_email)

        mock_validate_email.assert_called_once_with(
            invalid_email, check_deliverability=False
        )
        self.assertEqual(str(context.exception), "Invalid email: Invalid email format")

    @patch("dfm18.user.validate_email")
    def test_initialization_with_multiple_accounts(self, mock_validate_email: Mock):
        name_generated = self.faker.name()
        email_generated = self.faker.email()

        mock_validate_email.return_value = {"email": email_generated}

        user = User(name=name_generated, email=email_generated)

        account1 = Mock(spec=BankAccount)
        account2 = Mock(spec=BankAccount)

        account1.get_balance.return_value = 100.0
        account2.get_balance.return_value = 200.0

        user.add_account(account1)
        user.add_account(account2)

        self.assertEqual(len(user.accounts), 2)
        self.assertEqual(user.get_total_balance(), 300.0)

        account1.get_balance.assert_called_once()
        account2.get_balance.assert_called_once()
