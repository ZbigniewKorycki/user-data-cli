import unittest
from user_data_manager import UsersDataProcessor


class TestUsersDataProcessor(unittest.TestCase):

    def test_is_email_address_valid(self):
        # Test case: Valid email
        valid_email = "valid@example.com"
        self.assertTrue(UsersDataProcessor.is_email_address_valid(valid_email))

        # Test case: Valid email, extension with only alfa-numeric chars
        email_extension_with_alfa_num = "valid_email@example.a123"
        self.assertTrue(UsersDataProcessor.is_email_address_valid(email_extension_with_alfa_num))

        # Test case: Invalid email, without domain and extension
        email_no_domain_extension = "invalid_email@"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_no_domain_extension))

        # Test case: Invalid email, without @
        email_no_at_sign = "missing_at_sign.com"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_no_at_sign))

        # Test case: Invalid email, without dot between domain and extension
        email_without_dot = "no_dot@domaincom"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_without_dot))

        # Test case: Invalid email, without domain
        email_without_domain = "missing_domain@.com"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_without_domain))

        # Test case: Invalid email, @ in username
        email_at_sign_in_username = "inv@alid@example.com"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_at_sign_in_username))

        # Test case: Invalid email, @ in extension
        email_at_sign_in_extension = "invalid_email@example.@"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_at_sign_in_extension))

        # Test case: Invalid email, @ in domain
        email_at_sign_in_domain = "invalid_email@example.@"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_at_sign_in_domain))

        # Test case: Invalid email, extension with over 4 characters
        email_extension_over_four_char = "invalid_email@example.comnet"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_extension_over_four_char))

        # Test case: Invalid email, extension with no alfa-numeric char
        email_extension_with_no_alfa_num = "invalid_email@example.a1!d"
        self.assertFalse(UsersDataProcessor.is_email_address_valid(email_extension_with_no_alfa_num))

    def test_format_telephone_number(self):
        # Test case: phone with leading zeros
        phone_zeros = "00847940862"
        self.assertEqual("847940862", UsersDataProcessor.format_telephone_number(phone_zeros))

        # Test case: phone with plus and area code
        phone_plus_area_code = "+48844840862"
        self.assertEqual("844840862", UsersDataProcessor.format_telephone_number(phone_plus_area_code))

        # Test case: phone with area code in parentheses
        phone_area_code_in_parentheses = "(48)123123123"
        self.assertEqual("123123123",UsersDataProcessor.format_telephone_number(phone_area_code_in_parentheses))

        # Test case: phone with space
        phone_with_spaces = "123 123 123"
        self.assertEqual("123123123", UsersDataProcessor.format_telephone_number(phone_with_spaces))

        # Test case: phone with leading zeros and spaces
        phone_zeros_spaces = "00 123 123 123"
        self.assertEqual("123123123", UsersDataProcessor.format_telephone_number(phone_zeros_spaces))

        # Test case: phone correct format, nothing to change
        phone_correct = "123123123"
        self.assertEqual("123123123", UsersDataProcessor.format_telephone_number(phone_correct))
