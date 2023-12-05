from users_data_utils import UsersDataMerger


def process_users_data(files_paths):
    users_data_merger = UsersDataMerger(files_paths)
    users_data_merger.process_merged_users_data()
    return users_data_merger.df_merged_users_data


files = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]
