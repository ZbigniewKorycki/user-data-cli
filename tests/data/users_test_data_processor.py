from users_data_utils import UsersDataMerger, UsersDataExtractor, UsersDataFormatter
import os


def process_test_users_data():
    merger = UsersDataMerger(test_files_path)
    merged_data = merger.merge_data(UsersDataExtractor, UsersDataFormatter)
    merger.process_merged_users_data(merged_data)
    return merger.df_merged_users_data


test_files_path = [
    os.path.join(os.path.dirname(__file__), *path.split('/'))
    for path in [
        "test_data.xml",
        "test_data.csv",
        "test_data.json"
    ]
]

test_final_users_data = process_test_users_data()
