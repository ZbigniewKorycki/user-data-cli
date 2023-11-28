import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import Callable, List


class TelephoneFormatter:
    @staticmethod
    def format_number(number: str) -> str:
        pattern = r"\s|\+48|\(48\)|^00"
        return re.sub(pattern, "", number)


class EmailValidator:
    @staticmethod
    def is_valid(email: str) -> bool:
        validation_pattern = r"(^[^@]+@[^@]+\.[a-zA-Z\d]{1,4}$)"
        return True if re.match(validation_pattern, email) else False


class DataConverter:
    @staticmethod
    def xml_to_dict_list_with_email_and_phone_verification(
            path_to_xml: str,
            email_validator: Callable[[str], bool],
            telephone_formatter: Callable[[str], str],
    ) -> List[dict]:
        tree = ET.parse(path_to_xml)
        root = tree.getroot()
        data_dict = xmltodict.parse(ET.tostring(root))

        formatted_users_data = []
        for user in data_dict.get("users", {}).get("user", []):
            if (user.get("telephone_number") is None) or (
                    not email_validator(user.get("email", ""))
            ):
                continue
            else:
                user["telephone_number"] = telephone_formatter(
                    user.get("telephone_number", "")
                )
                formatted_users_data.append(user)
        return formatted_users_data

    @staticmethod
    def csv_to_dict_list_with_email_and_phone_verification(path_to_csv: str) -> List[dict]:
        pass

    @staticmethod
    def json_to_dict_list_with_email_and_phone_verification(path_to_json: str) -> List[dict]:
        pass
