from users_data_utils import UsersDataMerger, UsersDataExtractor, UsersDataFormatter


def process_users_data():
    merger = UsersDataMerger(files_path)
    merged_data = merger.merge_data(UsersDataExtractor, UsersDataFormatter)
    merger.process_merged_users_data(merged_data)
    return merger.df_merged_users_data


files_path = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]
