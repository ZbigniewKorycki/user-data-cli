from users_data_handler import UsersDataProcessor


def test_email_address_validation():

    valid_email = "valid@example.com"
    another_valid_email = "another_valid@gmail.com"
    invalid_email_no_domain_and_extension = "invalid_email@"
    invalid_email_with_missing_at_sign = "missing_at_sign.com"
    invalid_email_with_no_dot = "no_dot@domaincom"
    invalid_missing_domain = "missing_domain@.com"
    invalid_two_consecutive_at_sign = "invalid@@example.com"
    invalid_at_sign_in_extension = "invalid_email@example.@"
    valid_email_uppercase = "VALID@gmail.com"
    invalid_email_two_dots = "INVALID@..com"
    invalid_email_none = None

    assert UsersDataProcessor.is_email_address_valid(valid_email) is True
    assert UsersDataProcessor.is_email_address_valid(another_valid_email) is True
    assert UsersDataProcessor.is_email_address_valid(invalid_email_no_domain_and_extension) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_email_with_missing_at_sign) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_email_with_no_dot) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_missing_domain) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_two_consecutive_at_sign) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_at_sign_in_extension) is False
    assert UsersDataProcessor.is_email_address_valid(valid_email_uppercase) is True
    assert UsersDataProcessor.is_email_address_valid(invalid_email_two_dots) is False
    assert UsersDataProcessor.is_email_address_valid(invalid_email_none) is False


def test_telephone_formatter():
    phone_leading_zeros = "00847940862"
    phone_area_code_and_plus = "+48844840862"
    phone_area_code_in_parenthesis = "(48)123123123"
    phone_with_spaces = "123 123 123"
    phone_leading_zeros_and_spaces = "00 123 123 123"
    phone_correct = "123123123"

    assert UsersDataProcessor.format_telephone_number(phone_leading_zeros) == "847940862"
    assert UsersDataProcessor.format_telephone_number(phone_area_code_and_plus) == "844840862"
    assert UsersDataProcessor.format_telephone_number(phone_area_code_in_parenthesis) == "123123123"
    assert UsersDataProcessor.format_telephone_number(phone_with_spaces) == "123123123"
    assert UsersDataProcessor.format_telephone_number(phone_leading_zeros_and_spaces) == "123123123"
    assert UsersDataProcessor.format_telephone_number(phone_correct) == "123123123"