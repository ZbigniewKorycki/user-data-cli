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
