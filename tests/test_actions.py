import unittest
from actions import Actions
from data.users_test_data_processor import test_final_users_data
from unittest.mock import patch, call


@patch('actions.final_users_data', test_final_users_data)
class TestActions(unittest.TestCase):

    def test_authenticate_user(self):
        # Test case: Incorrect login, correct password for one of users
        action_incorrect_login = Actions(login='111111112', password='Wm&fkw9bI8')
        self.assertIs(action_incorrect_login.role, None)
        self.assertFalse(action_incorrect_login.authenticated_user)

        # Test case: Correct login, incorrect password
        action_incorrect_login = Actions(login='111111111', password='Wm&fkw9bI88')
        self.assertIs(action_incorrect_login.role, None)
        self.assertFalse(action_incorrect_login.authenticated_user)

        # Test case: Base user, login with tel
        action_base_by_tel = Actions(login='111111111', password='Wm&fkw9bI8')
        self.assertEqual(action_base_by_tel.role, "user")
        self.assertTrue(action_base_by_tel.authenticated_user)
        self.assertEqual(action_base_by_tel.login, '111111111')
        self.assertEqual(action_base_by_tel.password, 'Wm&fkw9bI8')

        # Test case: Base user, login with email
        action_base_by_email = Actions(login='test1@example.com', password='Wm&fkw9bI8')
        self.assertEqual(action_base_by_email.role, "user")
        self.assertTrue(action_base_by_email.authenticated_user)
        self.assertEqual(action_base_by_email.login, 'test1@example.com')
        self.assertEqual(action_base_by_email.password, 'Wm&fkw9bI8')

        # Test case: Admin, login with tel
        action_admin_by_tel = Actions(login='222222222', password='7GRMc-fg42')
        self.assertEqual(action_admin_by_tel.role, "admin")
        self.assertTrue(action_admin_by_tel.authenticated_user)
        self.assertEqual(action_admin_by_tel.login, '222222222')
        self.assertEqual(action_admin_by_tel.password, '7GRMc-fg42')

        # Test case: Admin, login with email
        action_admin_by_email = Actions(login='test2@example.com', password='7GRMc-fg42')
        self.assertEqual(action_admin_by_email.role, "admin")
        self.assertTrue(action_admin_by_email.authenticated_user)
        self.assertEqual(action_admin_by_email.login, 'test2@example.com')
        self.assertEqual(action_admin_by_email.password, '7GRMc-fg42')

    @patch('builtins.print')
    def test_print_all_accounts_base_user(self, mock_print):
        # Test case: Base user, login with tel
        action_unauthorized = Actions(login='111111111', password='Wm&fkw9bI8')
        action_unauthorized.print_all_accounts()
        mock_print.assert_called_with("Invalid Login")

    @patch('builtins.print')
    def test_print_all_accounts_admin(self, mock_print):
        # Test case: Admin
        action_admin = Actions(login='222222222', password='7GRMc-fg42')
        action_admin.print_all_accounts()
        mock_print.assert_called_with(10)

    @patch('builtins.print')
    def test_print_all_accounts_unauthenticated_user(self, mock_print):
        # Test case: unauthenticated user
        action_unauthorized = Actions(login='111111112', password='Wm&fkw9bI8')
        action_unauthorized.print_all_accounts()
        mock_print.assert_called_with("Invalid Login")

    @patch('builtins.print')
    def test_print_oldest_account_base_user(self, mock_print):
        # Test case: Base user
        action_unauthorized = Actions(login='111111111', password='Wm&fkw9bI8')
        action_unauthorized.print_oldest_account()
        mock_print.assert_called_with("Invalid Login")

    @patch('builtins.print')
    def test_print_oldest_account_admin(self, mock_print):
        # Test case: Admin, should return output base on user with data:
        # Test1;111111111;test1@example.com;Wm&fkw9bI8;user;2010-01-21 21:21:01;Adam (1)
        action_admin = Actions(login='222222222', password='7GRMc-fg42')
        action_admin.print_oldest_account()
        mock_print.assert_called_with("name: Test1\nemail_address: test1@example.com\ncreated_at: 2010-01-21 21:21:01")

    @patch('builtins.print')
    def test_group_by_age_base_user(self, mock_print):
        # Test case: Base user
        action_unauthorized = Actions(login='111111111', password='Wm&fkw9bI8')
        action_unauthorized.group_children_by_age()
        mock_print.assert_called_with("Invalid Login")

    @patch('builtins.print')
    def test_group_by_age_admin(self, mock_print):
        # Test case: Admin
        action_admin = Actions(login='222222222', password='7GRMc-fg42')
        action_admin.group_children_by_age()
        expected_calls = [
            call("age: 3, count: 2"),
            call("age: 14, count: 2"),
            call("age: 6, count: 3"),
            call("age: 9, count: 3"),
            call("age: 1, count: 4"),
        ]
        mock_print.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
