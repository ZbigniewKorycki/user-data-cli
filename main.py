from users_data_handler import UsersDataHandler
import pandas as pd

files_paths = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]


def merge_data(files_to_read: list[str]) -> list[dict]:
    merged_data = []
    for file in files_to_read:
        user = UsersDataHandler(file)
        merged_data.extend(user.process_users_data())
    return merged_data


def drop_duplicated_users_on_email(data):
    df = pd.DataFrame(data)
    df = df.sort_values(by="created_at", ascending=False)
    df_without_duplicated_email = df.drop_duplicates(subset=["email"], keep='first')
    return df_without_duplicated_email


def drop_duplicated_users_on_telephone(data):
    df = pd.DataFrame(data)
    df = df.sort_values(by="created_at", ascending=False)
    df_without_duplicated_phones = df.drop_duplicates(subset=["telephone_number"], keep='first')
    return df_without_duplicated_phones


def get_merged_data_after_removing_duplicates(files_to_read):
    merged_data = merge_data(files_to_read)
    data_after_removing_duplicated_emails = drop_duplicated_users_on_email(merged_data)
    data_after_removing_duplicated_telephones = drop_duplicated_users_on_telephone(
        data_after_removing_duplicated_emails)
    return data_after_removing_duplicated_telephones


merged_data = get_merged_data_after_removing_duplicates(files_paths)


def find_user(login, password):
    result = merged_data[
        ((merged_data["email"] == login) | (merged_data["telephone_number"] == login)) & (
                    merged_data["password"] == password)]
    return result


# user1 = find_user("jboyd@example.org", "_9tGfwed#7")
# user2 = user1.to_dict(orient="records")
# print(user2)
