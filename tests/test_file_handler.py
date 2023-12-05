import unittest
from unittest.mock import patch
from users_data_utils import UsersFileHandler


class TestUsersFileHandler(unittest.TestCase):

    def test_extract_file_extension(self):
        # Test case: Valid file path with extension
        file_handler = UsersFileHandler("/path/to/example.csv")
        self.assertEqual("csv", file_handler.extract_file_extension())

        # Test case: File path without extension
        file_handler_no_extension = UsersFileHandler("/path/to/example")
        self.assertIs(None, file_handler_no_extension.extract_file_extension())

    def test_read_csv(self):
        # Test case: Read valid csv test file
        file_handler = UsersFileHandler("./data/test_data.csv")
        users_data = file_handler.read_csv()
        self.assertIsInstance(users_data, list)
        for user in users_data:
            self.assertIsInstance(user, dict)
            self.assertIn("firstname", user)
            self.assertIn("telephone_number", user)
            self.assertIn("email", user)
            self.assertIn("password", user)
            self.assertIn("role", user)
            self.assertIn("created_at", user)
            self.assertIn("children", user)

    def test_read_json(self):
        # Test case: Read valid json test file
        file_handler = UsersFileHandler("./data/test_data.json")
        users_data = file_handler.read_json()
        self.assertIsInstance(users_data, list)
        for user in users_data:
            self.assertIsInstance(user, dict)
            self.assertIn("firstname", user)
            self.assertIn("telephone_number", user)
            self.assertIn("email", user)
            self.assertIn("password", user)
            self.assertIn("role", user)
            self.assertIn("created_at", user)
            self.assertIn("children", user)

    def test_parse_xml(self):
        # Test case: Parse valid xml, with direct reading of data inside ["users"]["user"]
        file_handler = UsersFileHandler("./data/test_data.xml")
        users_data = file_handler.parse_xml()
        self.assertIsInstance(users_data, list)
        for user in users_data:
            self.assertIsInstance(user, dict)
            self.assertIn("firstname", user)
            self.assertIn("telephone_number", user)
            self.assertIn("email", user)
            self.assertIn("password", user)
            self.assertIn("role", user)
            self.assertIn("created_at", user)
            self.assertIn("children", user)

    @patch('user_data_manager.UsersFileHandler.read_csv')
    def test_extract_data_csv(self, mock_read_csv_function):
        # Test case: extract data when file with csv extension
        file_handler_csv = UsersFileHandler("./data/test_data.csv")
        file_handler_csv.extract_data()
        mock_read_csv_function.assert_called_once()

    @patch('user_data_manager.UsersFileHandler.read_json')
    def test_extract_data_json(self, mock_read_json_function):
        # Test case: extract data when file with json extension
        file_handler_json = UsersFileHandler("./data/test_data.json")
        file_handler_json.extract_data()
        mock_read_json_function.assert_called_once()

    @patch('user_data_manager.UsersFileHandler.parse_xml')
    def test_extract_data_xml(self, mock_parse_xml_function):
        # Test case: extract data when file with xml extension
        file_handler_xml = UsersFileHandler("./data/test_data.xml")
        file_handler_xml.extract_data()
        mock_parse_xml_function.assert_called_once()

    def test_extract_data_unrecognized_extension(self):
        # Test case: extract data when unrecognized file extension
        file_handler = UsersFileHandler("./data/test_data.txt")
        result = file_handler.extract_data()
        self.assertIs(None, result)


if __name__ == '__main__':
    unittest.main()
