import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import List, Optional, Union
import csv
import json
import pandas as pd


class UsersFileHandler:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.file_extension = self.extract_file_extension()

    def extract_file_extension(self) -> Optional[str]:
        try:
            file_extension = self.path_to_file.rsplit(".", 1)[1]
        except IndexError:
            print(f"File extension not recognized in: {self.path_to_file}")
            return None
        else:
            return file_extension

    def extract_data(self) -> Optional[List[dict]]:
        if self.file_extension.lower() == "xml":
            return self.parse_xml()
        elif self.file_extension.lower() == "csv":
            return self.read_csv()
        elif self.file_extension.lower() == "json":
            return self.read_json()
        else:
            print(f"Given file extension ({self.file_extension}) is not supported.")
            return None

    def parse_xml(self) -> List[dict]:
        tree = ET.parse(self.path_to_file)
        root = tree.getroot()
        return xmltodict.parse(ET.tostring(root))["users"]["user"]

    def read_json(self) -> List[dict]:
        with open(self.path_to_file) as file:
            data = json.load(file)
        return data

    def read_csv(self) -> List[dict]:
        with open(self.path_to_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            data = list(reader)
        return data


class UsersDataProcessor:
    TELEPHONE_FORMATTING_PATTERN = r"\s|\+48|\(48\)|^00"
    EMAIL_VALIDATION_PATTERN = r"(^[^@]+@[^@\.]+\.[a-z\d]{1,4}$)"

    @staticmethod
    def filter_valid_data(data: List[dict]) -> List[dict]:
        return [user for user in data if user is not None]

    @classmethod
    def format_telephone_number(cls, number: str) -> str:
        return re.sub(cls.TELEPHONE_FORMATTING_PATTERN, "", number)

    @staticmethod
    def is_data_present_in_user(data: str, user: dict) -> bool:
        return True if data in user and user[data] not in ["", None, []] else False

    @classmethod
    def is_email_address_valid(cls, email: Union[str, dict]) -> bool:
        try:
            validation = re.match(cls.EMAIL_VALIDATION_PATTERN, email, re.IGNORECASE)
        except TypeError:
            return False
        else:
            return True if validation else False

    @classmethod
    def get_info_on_user_children(cls, user: dict) -> Optional[Union[dict, list]]:
        if not cls.is_data_present_in_user("children", user):
            return None
        if "child" in user["children"]:
            try:
                children_info = user["children"].get("child")
                return children_info if children_info is not None else user["children"]
            except AttributeError:
                return user["children"]
        else:
            try:
                children = [child.strip() for child in user["children"].split(",")]
            except AttributeError:
                return user["children"]
            else:
                children_info = [
                    {
                        "name": child.split("(")[0].strip(),
                        "age": int(child.split("(")[1].replace(")", "").strip()),
                    }
                    for child in children
                ]
                return children_info

    @classmethod
    def format_user_data(cls, user: dict) -> Optional[dict]:
        if not cls.is_data_present_in_user(
                "telephone_number", user
        ) or not cls.is_email_address_valid(user.get("email")):
            return None
        user["telephone_number"] = cls.format_telephone_number(user["telephone_number"])
        user["children"] = cls.get_info_on_user_children(user)
        return user

    @classmethod
    def process_data(cls, data: List[dict]) -> List[dict]:
        formatted_data = [cls.format_user_data(user) for user in data]
        validated_data = cls.filter_valid_data(formatted_data)
        return validated_data


class UsersDataHandler:
    def __init__(self, path_to_file: str):
        self.file_handler = UsersFileHandler(path_to_file)
        self.data_processor = UsersDataProcessor()

    def process_users_data(self) -> Optional[List[dict]]:
        try:
            data = self.file_handler.extract_data()
        except TypeError as e:
            print(e)
            return None
        else:
            try:
                processed_data = self.data_processor.process_data(data)
            except TypeError as e:
                print(e)
                return None
            else:
                return processed_data


class UsersDataMerger:

    def __init__(self, files_list: list):
        self.files_list = files_list
        self.merged_data = self.merge_users_data_from_multiple_files()

    def merge_users_data_from_multiple_files(self) -> List[dict]:
        merged_data = []
        for file in self.files_list:
            user = UsersDataHandler(file)
            if user.process_users_data() is not None:
                merged_data.extend(user.process_users_data())
        return merged_data

    def drop_duplicated_users_based_on_email(self):
        df = pd.DataFrame(self.merged_data)
        df = df.sort_values(by="created_at", ascending=False)
        df_without_duplicated_email = df.drop_duplicates(subset=["email"], keep='first')
        self.merged_data = df_without_duplicated_email

    def drop_duplicated_users_based_on_telephone_number(self):
        df = pd.DataFrame(self.merged_data)
        df = df.sort_values(by="created_at", ascending=False)
        df_without_duplicated_telephone_number = df.drop_duplicates(subset=["telephone_number"], keep='first')
        self.merged_data = df_without_duplicated_telephone_number

    def get_merged_data_without_duplicates(self):
        self.drop_duplicated_users_based_on_telephone_number()
        self.drop_duplicated_users_based_on_email()
        return self.merged_data
