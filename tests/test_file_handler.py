from users_data_handler import FileHandler


def test_extract_file_extension():
    # Test case: Valid file path with extension
    file_handler = FileHandler("/path/to/example.csv")
    assert file_handler.extract_file_extension() == "csv"

    # Test case: File path without extension
    file_handler_no_extension = FileHandler("/path/to/example")
    assert file_handler_no_extension.extract_file_extension() is None
