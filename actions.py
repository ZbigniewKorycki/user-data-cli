from process_users_data import process_users_data, files
import itertools
from typing import List
from db_connection import SQLiteConnection
from config import sqlite_config


class Actions:
    users_data = process_users_data(files)

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None
        self.user_data = None
        self.authenticate_user()

    def authenticate_user(self):
        try:
            user = Actions.users_data[
                (
                        (Actions.users_data["email"] == self.login)
                        | (Actions.users_data["telephone_number"] == self.login)
                )
                & (Actions.users_data["password"] == self.password)
                ].to_dict(orient="records")[0]
        except IndexError:
            self.authenticated_user = False
        else:
            self.authenticated_user = True
            self.role = user["role"]
            self.user_data = user

    @staticmethod
    def admin_required(func):
        def wrapper(self, *args, **kwargs):
            if self.role == "admin" and self.authenticated_user:
                return func(self, *args, **kwargs)
            else:
                print("Invalid Login")

        return wrapper

    @staticmethod
    def authentication_required(func):
        def wrapper(self, *args, **kwargs):
            if self.authenticated_user:
                return func(self, *args, **kwargs)
            else:
                print("Invalid Login")

        return wrapper

    @authentication_required
    def print_user_children(self):
        children = self.user_data["children"]
        if children:
            children.sort(key=lambda x: x["name"])
            for child in children:
                print(f"{child['name']}, {child['age']}")
        else:
            print(f"User with login: {self.login} has no children.")

    @authentication_required
    def find_users_with_similar_children_by_age(self):
        try:
            user_children_age = [child["age"] for child in self.user_data["children"]]
        except TypeError:
            print(f"User with login: {self.login} has no children. Can not find any matches.")
        else:
            users_with_children = Actions.users_data[Actions.users_data["children"].notna()]
            users_with_similar_children_age = users_with_children[
                users_with_children["children"].apply(
                    lambda x: (
                        any(
                            child["age"] in user_children_age
                            for child in x
                            if isinstance(child, dict)
                        )
                    )
                )
            ]
            similar_users = users_with_similar_children_age.to_dict(orient="records")
            for user in similar_users:
                if user["telephone_number"] == self.login or user["email"] == self.login:
                    continue
                children_sorted = sorted(user["children"], key=lambda x: x["name"])
                children_formatted = '; '.join(f"{child['name']}, {child['age']}" for child in children_sorted)
                print(f"{user['firstname']}, {user['telephone_number']}: {children_formatted}")

    @admin_required
    def print_all_accounts(self):
        print(len(Actions.users_data))

    @admin_required
    def print_oldest_account(self):
        oldest_account = Actions.users_data.sort_values(by="created_at").to_dict(
            orient="records"
        )[0]
        if oldest_account is not None:
            print(
                f"name: {oldest_account['firstname']}\n"
                f"email_address: {oldest_account['email']}\n"
                f"created_at: {oldest_account['created_at']}"
            )

    @admin_required
    def group_children_by_age(self):
        children_data = Actions.users_data["children"].to_list()
        filtered_children_without_none = [
            child for child in children_data if child is not None
        ]
        children = []
        for user_children in filtered_children_without_none:
            for child in user_children:
                if isinstance(child["age"], int):
                    children.append(child["age"])
        sorted_data = sorted(children)
        grouped_data = sorted(
            [
                {"age": key, "count": len(list(group))}
                for key, group in itertools.groupby(sorted_data)
            ],
            key=lambda x: x["count"],
        )
        for child in grouped_data:
            print(f"age: {child['age']}, count: {child['count']}")

    @admin_required
    def create_database(self):
        db_conn = SQLiteConnection(sqlite_config.db_file)
        for index, row in Actions.users_data.iterrows():
            db_conn.execute_query(
                "INSERT INTO users_data (email, firstname, telephone_number, password, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (row['email'], row['firstname'], row['telephone_number'], row['password'], row['role'],
                 row['created_at'])
            )
            if row["children"] is not None:
                for child in row["children"]:
                    db_conn.execute_query(
                        "INSERT INTO users_children (parent_email, child_name, child_age) VALUES (?, ?, ?)",
                        (row['email'], child['name'], child['age'])
                    )
