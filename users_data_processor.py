from users_data_utils import UsersDataMerger, UsersDataExtractor, UsersDataFormatter
import os


def process_users_data():
    merger = UsersDataMerger(files_path)
    merged_data = merger.merge_data(UsersDataExtractor, UsersDataFormatter)
    merger.process_merged_users_data(merged_data)
    return merger.df_merged_users_data


files_path = [
    os.path.join(os.path.dirname(__file__), *path.split("/"))
    for path in [
        "data/a/b/users_1.xml",
        "data/users_2.xml",
        "data/a/b/users_1.csv",
        "data/a/c/users_2.csv",
        "data/a/users.json",
    ]
]

final_users_data = process_users_data()
