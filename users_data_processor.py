from users_data_utils import UsersDataMerger, UsersDataExtractor, UsersDataFormatter


def process_users_data():
    merged_data = []
    for path in files_path:
        extracted_data = UsersDataExtractor(path).extract_data()
        formatted_data = UsersDataFormatter(extracted_data).process_data()
        if formatted_data:
            merged_data.extend(formatted_data)
    return UsersDataMerger.process_merged_users_data(merged_data)


files_path = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]
