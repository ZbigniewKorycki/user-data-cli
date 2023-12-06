from users_data_utils import UsersDataMerger, UsersDataExtractor, UsersDataFormatter
import os
from pandas import DataFrame


def process_users_data(files_path) -> DataFrame:
    try:
        merged_data = UsersDataMerger.merge_data(files_path, UsersDataExtractor, UsersDataFormatter)
        final_data = UsersDataMerger.process_merged_users_data(merged_data)
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return DataFrame()
    else:
        return final_data


paths = [
    os.path.join(os.path.dirname(__file__), *path.split("/"))
    for path in [
        "data/a/b/users_1.xml",
        "data/users_2.xml",
        "data/a/b/users_1.csv",
        "data/a/c/users_2.csv",
        "data/a/users.json",
    ]
]

final_users_data = process_users_data(paths)
