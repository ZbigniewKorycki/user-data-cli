import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import List
import csv
import json


class TelephoneHandler:
    FORMATTING_PATTERN = r"\s|\+48|\(48\)|^00"

    @classmethod
    def format_number(cls, number: str) -> str:
        return re.sub(cls.FORMATTING_PATTERN, "", number)

    @staticmethod
    def is_present(number: str) -> bool:
        return False if (number == "") or (number is None) or (number == []) else True


class EmailHandler:
    VALIDATION_PATTERN = r"(^[^@]+@[^@\.]+\.[a-z\d]{1,4}$)"

    @classmethod
    def is_valid(cls, email: str) -> bool:
        return True if re.match(cls.VALIDATION_PATTERN, email, re.IGNORECASE) else False


class FileHandler:

    @staticmethod
    def extract_file_extension_from_path(path_to_file: str) -> str:
        return path_to_file.rsplit(".", 1)[1]


class DataConverter:
    @staticmethod
    def xml_to_dict_list_with_email_and_phone_verification(
            path_to_xml: str,
    ) -> List[dict]:
        tree = ET.parse(path_to_xml)
        root = tree.getroot()
        data_dict = xmltodict.parse(ET.tostring(root))

        formatted_users_data = []
        for user in data_dict.get("users", {}).get("user", []):
            if (user.get("telephone_number") is None) or (
                    not EmailHandler.is_valid(user["email"])
            ):
                continue
            user["telephone_number"] = EmailHandler.format_number(
                user["telephone_number"]
            )
            if user["children"]:
                user["children"] = user["children"]["child"]
            else:
                user["children"] = None
            formatted_users_data.append(user)
        return formatted_users_data

    @staticmethod
    def csv_to_dict_list_with_email_and_phone_verification(
            path_to_csv: str,
    ) -> List[dict]:
        users_data = []
        with open(path_to_csv, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                children = []
                if row["children"]:
                    children_info = [
                        child.strip() for child in row["children"].split(",")
                    ]
                    children = [
                        {
                            "name": info.split("(")[0].strip(),
                            "age": int(info.split("(")[1].replace(")", "").strip()),
                        }
                        for info in children_info
                    ]
                else:
                    children = None
                email = row.get("email", "")
                telephone = row.get("telephone_number", "")
                if EmailHandler.is_valid(email) and telephone != "":
                    telephone = TelephoneHandler.format_number(telephone)
                    user = {
                        "firstname": row.get("firstname", ""),
                        "telephone_number": telephone,
                        "email": email,
                        "password": row.get("password", ""),
                        "role": row.get("role", ""),
                        "created_at": row.get("created_at", ""),
                        "children": children,
                    }
                    users_data.append(user)
                else:
                    continue
            return users_data

    @staticmethod
    def json_to_dict_list_with_email_and_phone_verification(
            path_to_json: str,
    ) -> List[dict]:
        user_data = []
        with open(path_to_json) as file:
            data = json.load(file)
            for user in data:
                if user["telephone_number"] != "" and EmailHandler.is_valid(
                        user["email"]
                ):
                    user["telephone_number"] = TelephoneHandler.format_number(
                        user["telephone_number"]
                    )
                    if not user["children"]:
                        user["children"] = None
                    user_data.append(user)
                else:
                    continue
        return user_data
