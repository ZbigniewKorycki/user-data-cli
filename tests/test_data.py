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

    