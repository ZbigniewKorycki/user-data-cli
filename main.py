from users_data_handler import UsersDataHandler
import pandas as pd

files_to_read = [
    "data/a/b/users_1.xml",
    "data/users_2.xml",
    "data/a/b/users_1.csv",
    "data/a/c/users_2.csv",
    "data/a/users.json"
]

data = []
for file in files_to_read:
    user = UsersDataHandler(file)
    data.extend(user.process_users_data())

df = pd.DataFrame(data)
df = df.sort_values(by="created_at", ascending=False)
df_without_duplicated_email = df.drop_duplicates(subset=["email"], keep='first')
df_without_duplicated_phones = df_without_duplicated_email.drop_duplicates(subset=["telephone_number"], keep='first')

print(df_without_duplicated_phones)