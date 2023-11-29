import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import List
import csv
import json
from scripts import logging_setup

logger = logging_setup.setup_logging(__name__)


class TelephoneHandler:
    FORMATTING_PATTERN = r"\s|\+48|\(48\)|^00"

    @classmethod
    def format_number(cls, number: str) -> str:
        return re.sub(cls.FORMATTING_PATTERN, "", number)

    @staticmethod
    def is_phone_present(number) -> bool:
        return False if (number == "") or (number is None) or (number == []) else True


class EmailHandler:
    VALIDATION_PATTERN = r"(^[^@]+@[^@\.]+\.[a-z\d]{1,4}$)"

    @classmethod
    def is_email_valid(cls, email) -> bool:
        try:
            validation = re.match(cls.VALIDATION_PATTERN, email, re.IGNORECASE)
        except TypeError:
            logger.debug("TypeError in email validation")
            return False
        else:
            return True if validation else False


class DataConverter:

    @staticmethod
    def extract_file_extension_from_path(path_to_file: str) -> str:
        return path_to_file.rsplit(".", 1)[1]

    @staticmethod
    def parse_xml_to_dict(path_to_xml: str) -> dict:
        tree = ET.parse(path_to_xml)
        root = tree.getroot()
        return xmltodict.parse(ET.tostring(root))

    @staticmethod
    def format_user_from_xml(user: dict):
        if not TelephoneHandler.is_phone_present(user.get("telephone_number")) or not EmailHandler.is_email_valid(
                user.get("email")):
            return None
        user["telephone_number"] = TelephoneHandler.format_number(user["telephone_number"])
        user["children"] = user["children"].get("child") if user.get("children") else None
        return user

    @staticmethod
    def filter_valid_users_from_xml(data: List[dict]) -> List[dict]:
        return [DataConverter.format_user_from_xml(user) for user in data if
                DataConverter.format_user_from_xml(user)]

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
                if EmailHandler.is_email_valid(email) and telephone != "":
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
                if user["telephone_number"] != "" and EmailHandler.is_email_valid(
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
