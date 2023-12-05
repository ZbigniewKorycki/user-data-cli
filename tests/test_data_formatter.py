import unittest
from users_data_utils import UsersDataFormatter


class TestUsersDataFormatter(unittest.TestCase):
    def test_is_email_address_valid(self):
        # Test case: Valid email
        valid_email = "valid@example.com"
        self.assertTrue(UsersDataFormatter.is_email_address_valid(valid_email))

        # Test case: Valid email, extension with only alfa-numeric chars
        email_extension_with_alfa_num = "valid_email@example.a123"
        self.assertTrue(
            UsersDataFormatter.is_email_address_valid(email_extension_with_alfa_num)
        )

        # Test case: Invalid email, without domain and extension
        email_no_domain_extension = "invalid_email@"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_no_domain_extension)
        )

        # Test case: Invalid email, without @
        email_no_at_sign = "missing_at_sign.com"
        self.assertFalse(UsersDataFormatter.is_email_address_valid(email_no_at_sign))

        # Test case: Invalid email, without dot between domain and extension
        email_without_dot = "no_dot@domaincom"
        self.assertFalse(UsersDataFormatter.is_email_address_valid(email_without_dot))

        # Test case: Invalid email, without domain
        email_without_domain = "missing_domain@.com"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_without_domain)
        )

        # Test case: Invalid email, @ in username
        email_at_sign_in_username = "inv@alid@example.com"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_at_sign_in_username)
        )

        # Test case: Invalid email, @ in extension
        email_at_sign_in_extension = "invalid_email@example.@"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_at_sign_in_extension)
        )

        # Test case: Invalid email, @ in domain
        email_at_sign_in_domain = "invalid_email@example.@"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_at_sign_in_domain)
        )

        # Test case: Invalid email, extension with over 4 characters
        email_extension_over_four_char = "invalid_email@example.comnet"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_extension_over_four_char)
        )

        # Test case: Invalid email, extension with no alfa-numeric char
        email_extension_with_no_alfa_num = "invalid_email@example.a1!d"
        self.assertFalse(
            UsersDataFormatter.is_email_address_valid(email_extension_with_no_alfa_num)
        )

    def test_format_telephone_number(self):
        # Test case: phone with leading zeros
        phone_zeros = "00847940862"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_zeros), "847940862"
        )

        # Test case: phone with plus and area code
        phone_plus_area_code = "+48844840862"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_plus_area_code),
            "844840862",
        )

        # Test case: phone with area code in parentheses
        phone_area_code_in_parentheses = "(48)123123123"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_area_code_in_parentheses),
            "123123123",
        )

        # Test case: phone with space
        phone_with_spaces = "123 123 123"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_with_spaces), "123123123"
        )

        # Test case: phone with leading zeros and spaces
        phone_zeros_spaces = "00 123 123 123"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_zeros_spaces), "123123123"
        )

        # Test case: phone correct format, nothing to change
        phone_correct = "123123123"
        self.assertEqual(
            UsersDataFormatter.format_telephone_number(phone_correct), "123123123"
        )

    def test_filter_valid_data(self):
        # Test case: valid test data as list of dict
        test_data = [{"name": "user1"}, None, {"name": "user2"}, None]
        self.assertEqual(len(UsersDataFormatter.filter_valid_data(test_data)), 2)
        self.assertIsInstance(UsersDataFormatter.filter_valid_data(test_data), list)

        # Test case: valid test data as list of None values
        test_data1 = [None, None, None, None]
        self.assertEqual(len(UsersDataFormatter.filter_valid_data(test_data1)), 0)
        self.assertIsInstance(UsersDataFormatter.filter_valid_data(test_data1), list)

    def test_is_data_present_in_user(self):
        test_user = {
            "firstname": "test",
            "telephone_number": "",
            "email": None,
            "password": "test_password",
            "role": "user",
            "created_at": "2023-04-02 15:57:34",
            "children": [],
        }
        # Test case: check if email of value None is recognized as not present
        self.assertFalse(UsersDataFormatter.is_data_present_in_user("email", test_user))

        # Test case: check if phone of value "" is recognized as not present
        self.assertFalse(
            UsersDataFormatter.is_data_present_in_user("telephone_number", test_user)
        )

        # Test case: check if children of value [] is recognized as not present
        self.assertFalse(
            UsersDataFormatter.is_data_present_in_user("children", test_user)
        )

        # Test case: check if role of value "user" is recognized as present
        self.assertTrue(UsersDataFormatter.is_data_present_in_user("role", test_user))

    def test_get_info_on_user_children(self):
        # Test case: User with no children, from csv format
        user_no_children_csv = {"firstname": "Test", "children": ""}
        children_info_zero_csv = UsersDataFormatter.get_info_on_user_children(
            user_no_children_csv
        )
        self.assertIs(children_info_zero_csv, None)

        # Test case: User with one child, from csv format
        user_one_child_csv = {"firstname": "Test", "children": "Adam (1)"}
        children_info_one_csv = UsersDataFormatter.get_info_on_user_children(
            user_one_child_csv
        )
        self.assertEqual(children_info_one_csv, [{"name": "Adam", "age": "1"}])

        # Test case: User with three children, from csv format
        user_three_children_csv = {
            "firstname": "Test",
            "children": "Adam (1),Hellen (3),Peter (13)",
        }
        children_info_three_csv = UsersDataFormatter.get_info_on_user_children(
            user_three_children_csv
        )
        self.assertEqual(
            children_info_three_csv,
            [
                {"name": "Adam", "age": "1"},
                {"name": "Hellen", "age": "3"},
                {"name": "Peter", "age": "13"},
            ],
        )

        # Test case: User with no children, from json format
        user_no_children_json = {"firstname": "Test", "children": []}
        children_info_zero_json = UsersDataFormatter.get_info_on_user_children(
            user_no_children_json
        )
        self.assertIs(children_info_zero_json, None)

        # Test case: User with one child, from json format
        user_one_children_json = {
            "firstname": "Test",
            "children": [{"name": "Test", "age": 18}],
        }
        children_info_one_json = UsersDataFormatter.get_info_on_user_children(
            user_one_children_json
        )
        self.assertEqual(children_info_one_json, [{"name": "Test", "age": 18}])

        # Test case: User with three children, from json format
        user_three_children_json = {
            "firstname": "Test",
            "children": [
                {"name": "Test1", "age": 17},
                {"name": "Test2", "age": 8},
                {"name": "Test3", "age": 11},
            ],
        }
        children_info_three_json = UsersDataFormatter.get_info_on_user_children(
            user_three_children_json
        )
        self.assertEqual(
            children_info_three_json,
            [
                {"name": "Test1", "age": 17},
                {"name": "Test2", "age": 8},
                {"name": "Test3", "age": 11},
            ],
        )

        # Test case: User with no children, from xml format
        user_no_children_xml = {"firstname": "Test", "children": None}
        children_info_zero_xml = UsersDataFormatter.get_info_on_user_children(
            user_no_children_xml
        )
        self.assertIs(children_info_zero_xml, None)

        # Test case: User with one child, from xml format
        user_one_children_xml = {
            "firstname": "Test",
            "children": {"child": {"name": "Teresa", "age": "4"}},
        }
        children_info_one_xml = UsersDataFormatter.get_info_on_user_children(
            user_one_children_xml
        )
        self.assertEqual(children_info_one_xml, [{"name": "Teresa", "age": "4"}])

        # Test case: User with three children, from xml format
        user_three_children_xml = {
            "firstname": "Test",
            "children": {
                "child": [
                    {"name": "Jennifer", "age": 2},
                    {"name": "Adam", "age": 1},
                    {"name": "Omar", "age": 10},
                ]
            },
        }
        children_info_three_xml = UsersDataFormatter.get_info_on_user_children(
            user_three_children_xml
        )
        self.assertEqual(
            children_info_three_xml,
            [
                {"name": "Jennifer", "age": 2},
                {"name": "Adam", "age": 1},
                {"name": "Omar", "age": 10},
            ],
        )

    def test_convert_children_age_to_int(self):
        # Test case: one child,  age as str
        test_children_data_one = [{"name": "Adam", "age": "11"}]
        result_after_conversion_one = UsersDataFormatter.convert_children_age_to_int(
            test_children_data_one
        )
        self.assertEqual(result_after_conversion_one, [{"name": "Adam", "age": 11}])

        # Test case: three children, mixed type int/str
        test_children_data_three = [
            {"name": "Adam", "age": "1"},
            {"name": "Alex", "age": 2},
            {"name": "Bob", "age": "4"},
        ]
        result_after_conversion_three = UsersDataFormatter.convert_children_age_to_int(
            test_children_data_three
        )
        self.assertEqual(
            result_after_conversion_three,
            [
                {"name": "Adam", "age": 1},
                {"name": "Alex", "age": 2},
                {"name": "Bob", "age": 4},
            ],
        )

        # Test case: one child, invalid str to num
        test_children_data_one_invalid = [{"name": "Adam", "age": "one"}]
        result_after_conversion_invalid = (
            UsersDataFormatter.convert_children_age_to_int(
                test_children_data_one_invalid
            )
        )
        self.assertEqual(
            test_children_data_one_invalid, [{"name": "Adam", "age": "one"}]
        )

    def test_format_user_data(self):
        # Test case: valid user data, number to format, children data to format
        test_user_valid = {
            "firstname": "Test",
            "telephone_number": "+48123123123",
            "email": "example@gmail.com",
            "password": "pass23451#",
            "role": "admin",
            "created_at": "2023-11-19 20:42:33",
            "children": "Michael (12),Theresa (6),Judith (1)",
        }
        result_test_user_valid = UsersDataFormatter.format_user_data(test_user_valid)
        self.assertEqual(
            result_test_user_valid,
            {
                "firstname": "Test",
                "telephone_number": "123123123",
                "email": "example@gmail.com",
                "password": "pass23451#",
                "role": "admin",
                "created_at": "2023-11-19 20:42:33",
                "children": [
                    {"name": "Michael", "age": 12},
                    {"name": "Theresa", "age": 6},
                    {"name": "Judith", "age": 1},
                ],
            },
        )

        # Test case: invalid user data, no tel number
        test_user_invalid_no_tel = {
            "firstname": "Test",
            "telephone_number": "",
            "email": "example@gmail.com",
            "password": "pass23451#",
            "role": "admin",
            "created_at": "2023-11-19 20:42:33",
            "children": "Michael (12),Theresa (6),Judith (1)",
        }
        result_test_user_invalid_no_tel = UsersDataFormatter.format_user_data(
            test_user_invalid_no_tel
        )
        self.assertIs(result_test_user_invalid_no_tel, None)

        # Test case: invalid user data, invalid email - with two @
        test_user_invalid_email = {
            "firstname": "Test",
            "telephone_number": "123123123",
            "email": "example@@gmail.com",
            "password": "pass23451#",
            "role": "admin",
            "created_at": "2023-11-19 20:42:33",
            "children": "Michael (12),Theresa (6),Judith (1)",
        }
        result_test_user_invalid_email = UsersDataFormatter.format_user_data(
            test_user_invalid_email
        )
        self.assertIs(result_test_user_invalid_email, None)


if __name__ == "__main__":
    unittest.main()
