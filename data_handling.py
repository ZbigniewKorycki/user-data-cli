import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import Callable, List
import csv


class TelephoneFormatter:
    @staticmethod
    def format_number(number: str) -> str:
        pattern = r"\s|\+48|\(48\)|^00"
        return re.sub(pattern, "", number)


class EmailValidator:
    @staticmethod
    def is_valid(email: str) -> bool:
        validation_pattern = r"(^[^@]+@[^@]+\.[a-z\d]{1,4}$)"
        return True if re.match(validation_pattern, email, re.IGNORECASE) else False


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
        users_data = []
        with open(path_to_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                children = []
                if row.get('children'):
                    children_info = [child.strip() for child in row['children'].split(',')]
                    children = [
                        {'name': info.split('(')[0].strip(), 'age': int(info.split('(')[1].replace(')', '').strip())}
                        for
                        info in children_info]
                email = row.get('email', '')
                telephone = row.get('telephone_number', '')
                if EmailValidator.is_valid(email) and telephone != '':
                    telephone = TelephoneFormatter.format_number(telephone)
                    user = {
                        'firstname': row.get('firstname', ''),
                        'telephone_number': telephone,
                        'email': email,
                        'password': row.get('password', ''),
                        'role': row.get('role', ''),
                        'created_at': row.get('created_at', ''),
                        'children': children
                    }
                    users_data.append(user)
                else:
                    continue
            return users_data

    @staticmethod
    def json_to_dict_list_with_email_and_phone_verification(path_to_json: str) -> List[dict]:
        pass
