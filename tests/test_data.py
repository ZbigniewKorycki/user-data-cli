import re


def test_phone_formatting():
    sub_pattern = r"\s|\+48|\(48\)|^00"

    phone_with_leading_zeros = "00847940862"
    phone_with_area_code_and_plus = "+48844840862"
    phone_with_area_code_in_parenthesis = "(48)123123123"
    phone_with_spaces = "123 123 123"
    phone_with_leading_zeros_and_spaces = "00 123 123 123"

    assert re.sub(sub_pattern, "", phone_with_leading_zeros) == "847940862"
    assert re.sub(sub_pattern, "", phone_with_area_code_and_plus) == "844840862"
    assert re.sub(sub_pattern, "", phone_with_area_code_in_parenthesis) == "123123123"
    assert re.sub(sub_pattern, "", phone_with_spaces) == "123123123"
    assert re.sub(sub_pattern, "", phone_with_leading_zeros_and_spaces) == "123123123"


def test_email_validator():
    validation_pattern = r"(^[^@]+@[^@]+\.[a-zA-Z\d]{1,4}$)"

    valid_email = "valid@example.com"
    another_valid_email = "another_valid@gmail.com"
    invalid_email_no_domain_and_extension = "invalid_email@"
    invalid_email_with_missing_at_sign = "missing_at_sign.com"
    invalid_email_with_no_dot = "no_dot@domaincom"
    invalid_missing_domain = "missing_domain@.com"
    invalid_two_consecutive_at_sign_ = "invalid@@example.com"
    invalid_at_sign_in_extension = "invalid_email@example.@"

    assert re.match(validation_pattern, valid_email) is not None
    assert re.match(validation_pattern, another_valid_email) is not None
    assert re.match(validation_pattern, invalid_email_no_domain_and_extension) is None
    assert re.match(validation_pattern, invalid_email_with_missing_at_sign) is None
    assert re.match(validation_pattern, invalid_email_with_no_dot) is None
    assert re.match(validation_pattern, invalid_missing_domain) is None
    assert re.match(validation_pattern, invalid_two_consecutive_at_sign_) is None
    assert re.match(validation_pattern, invalid_at_sign_in_extension) is None
