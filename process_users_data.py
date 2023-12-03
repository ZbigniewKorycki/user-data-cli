from user_data_manager import UsersDataMerger


def process_users_data(files_paths):
    users_data_merger = UsersDataMerger(files_paths)
    return users_data_merger.get_merged_data_without_duplicates()


files = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]
