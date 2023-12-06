import re
import xmltodict
import xml.etree.ElementTree as ET
from typing import List, Optional
import csv
import json
import pandas as pd
from pandas import DataFrame


class UsersDataExtractor:
    def __init__(self, path_to_file: str):
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
        if self.file_extension == "xml":
            return self.parse_xml()
        elif self.file_extension == "csv":
            return self.read_csv()
        elif self.file_extension == "json":
            return self.read_json()
        else:
            print(f"File extension ({self.file_extension}) is not supported.")
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


class UsersDataFormatter:
    TELEPHONE_FORMATTING_PATTERN = r"\s|\+48|\(48\)|^00"
    EMAIL_VALID_PATTERN = r"(^[^@]+@[^@\.]+\.[a-z\d]{1,4}$)"

    def __init__(self, data_to_format: List[dict]):
        self.data = data_to_format

    @staticmethod
    def filter_data(data: List[dict]) -> List[dict]:
        return [user for user in data if user is not None]

    @classmethod
    def format_tel_num(cls, number: str) -> str:
        return re.sub(cls.TELEPHONE_FORMATTING_PATTERN, "", number)

    @staticmethod
    def is_data_present(key: str, user: dict) -> bool:
        return True if key in user and user[key] not in ["", None, []] else False

    @classmethod
    def is_email_valid(cls, email: str) -> bool:
        try:
            result = re.match(cls.EMAIL_VALID_PATTERN, email, re.IGNORECASE)
        except TypeError:
            return False
        else:
            return True if result else False

    @classmethod
    def get_info_on_user_children(cls, user: dict) -> Optional[List[dict]]:
        if not cls.is_data_present("children", user):
            return None
        children_data = user.get("children", "")
        # Check if children from users data type xml
        if isinstance(children_data, dict):
            if isinstance(children_data.get("child"), dict):
                return [children_data["child"]]
            elif isinstance(children_data.get("child"), list):
                return [child for child in children_data["child"]]
            else:
                return None
        # Check if children from users data type json
        elif isinstance(children_data, list):
            return list(children_data)
        # Else children from users data type csv
        else:
            children = [child.strip() for child in children_data.split(",")]
            return [
                {
                    "name": child.split("(")[0].strip(),
                    "age": child.split("(")[1].replace(")", "").strip(),
                }
                for child in children
                if child != ""
            ]

    @staticmethod
    def children_age_to_int(children_data: List[dict]) -> Optional[List[dict]]:
        if children_data is not None:
            for child in children_data:
                try:
                    child["age"] = int(child["age"])
                except (ValueError, KeyError):
                    print(f"Incorrect format of child age: {child}")
        return children_data

    @classmethod
    def format_user_data(cls, user: dict) -> Optional[dict]:
        if not cls.is_data_present("telephone_number", user) or not cls.is_email_valid(
                user.get("email")
        ):
            return None
        user["telephone_number"] = cls.format_tel_num(user["telephone_number"])
        user["children"] = cls.get_info_on_user_children(user)
        user["children"] = cls.children_age_to_int(user["children"])
        return user

    def process_data(self) -> Optional[List[dict]]:
        try:
            format_data = [
                UsersDataFormatter.format_user_data(user) for user in self.data
            ]
            valid_data = UsersDataFormatter.filter_data(format_data)
        except Exception as e:
            print(f"Encounter error while processing data {e}")
            return None
        return valid_data


class UsersDataMerger:

    @staticmethod
    def merge_data(files_path: List[str], data_extractor, data_formatter) -> List[dict]:
        merged_data = []
        for path in files_path:
            extracted_data = data_extractor(path).extract_data()
            formatted_data = data_formatter(extracted_data).process_data()
            if formatted_data:
                merged_data.extend(formatted_data)
        return merged_data

    @staticmethod
    def process_merged_users_data(merged_data: List[dict]) -> DataFrame:
        try:
            df_merged_data = pd.DataFrame(merged_data)
            if not df_merged_data.empty:
                df_merged_data = df_merged_data.sort_values(
                    by="created_at", ascending=False
                )
                df_merged_data.drop_duplicates(
                    subset=["telephone_number"], keep="first", inplace=True
                )
                df_merged_data.drop_duplicates(
                    subset=["email"], keep="first", inplace=True
                )
        except Exception as e:
            print(f"Encounter error while processing merged data: {e}")
            return DataFrame()
        else:
            return df_merged_data
