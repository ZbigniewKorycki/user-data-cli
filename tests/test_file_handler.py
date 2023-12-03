import unittest
from users_data_handler import FileHandler


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_extract_file_extension(self):
        # Test case: Valid file path with extension
        file_handler = FileHandler("/path/to/example.csv")
        self.assertEqual("csv", file_handler.extract_file_extension())

        # Test case: File path without extension
        file_handler_no_extension = FileHandler("/path/to/example")
        self.assertIs(None, file_handler_no_extension.extract_file_extension())

    def test_read_csv_file(self):
        # Test case: Read csv test file
        file_handler = FileHandler("./data/test_data.csv")
        users_data = file_handler.read_csv_file()
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

    def test_read_json_file(self):
        # Test case: Read json test file
        file_handler = FileHandler("./data/test_data.json")
        users_data = file_handler.read_json_file()
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
