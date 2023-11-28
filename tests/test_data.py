from data_handling import TelephoneFormatter, EmailValidator


def test_email_address_validation():
    valid_email = "valid@example.com"
    another_valid_email = "another_valid@gmail.com"
    invalid_email_no_domain_and_extension = "invalid_email@"
    invalid_email_with_missing_at_sign = "missing_at_sign.com"
    invalid_email_with_no_dot = "no_dot@domaincom"
    invalid_missing_domain = "missing_domain@.com"
    invalid_two_consecutive_at_sign = "invalid@@example.com"
    invalid_at_sign_in_extension = "invalid_email@example.@"

    assert EmailValidator.is_valid(valid_email) is True
    assert EmailValidator.is_valid(another_valid_email) is True
    assert EmailValidator.is_valid(invalid_email_no_domain_and_extension) is False
    assert EmailValidator.is_valid(invalid_email_with_missing_at_sign) is False
    assert EmailValidator.is_valid(invalid_email_with_no_dot) is False
    assert EmailValidator.is_valid(invalid_missing_domain) is False
    assert EmailValidator.is_valid(invalid_two_consecutive_at_sign) is False
    assert EmailValidator.is_valid(invalid_at_sign_in_extension) is False


def test_telephone_formatter():
    phone_leading_zeros = "00847940862"
    phone_area_code_and_plus = "+48844840862"
    phone_area_code_in_parenthesis = "(48)123123123"
    phone_with_spaces = "123 123 123"
    phone_leading_zeros_and_spaces = "00 123 123 123"
    phone_correct = "123123123"

    assert TelephoneFormatter.format_number(phone_leading_zeros) == "847940862"
    assert TelephoneFormatter.format_number(phone_area_code_and_plus) == "844840862"
    assert TelephoneFormatter.format_number(phone_area_code_in_parenthesis) == "123123123"
    assert TelephoneFormatter.format_number(phone_with_spaces) == "123123123"
    assert TelephoneFormatter.format_number(phone_leading_zeros_and_spaces) == "123123123"
    assert TelephoneFormatter.format_number(phone_correct) == "123123123"
