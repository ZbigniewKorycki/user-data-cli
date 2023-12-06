from users_data_processor import final_users_data
from config.db_config import db
import itertools
import os.path
import sqlite3
from sqlite3 import Cursor, Connection
from typing import Optional, List
from pandas import DataFrame


class Actions:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None
        self.db_available = Actions.is_db_available(db)
        self.authenticate_user()

    def authenticate_user(self):
        if self.db_available:
            self.authenticate_user_with_db()
        else:
            user = self.get_data_of_user()
            if user:
                self.authenticated_user = True
                self.role = self.get_role_of_logged_user()

    def authenticate_user_with_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                role = self.get_role_of_logged_user_db(cursor)
                if role:
                    self.authenticated_user = True
                    self.role = role
        except sqlite3.Error:
            print("Error while authenticating user.")

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

    @staticmethod
    def is_db_available(db_path: str) -> bool:
        return True if os.path.exists(db_path) else False

    @authentication_required
    def print_children(self):
        if self.db_available:
            self.print_children_db()
        else:
            user_children = self.get_children_of_logged_user()
            if user_children:
                user_children.sort(key=lambda x: x["name"])
                for child in user_children:
                    print(f"{child['name']}, {child['age']}")
            else:
                print(f"User with login: {self.login} has no children.")

    @authentication_required
    def print_children_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                children_of_user = self.get_children_of_logged_user_db(cursor)
                if children_of_user:
                    children_of_user.sort(key=lambda x: x["name"])
                    for child in children_of_user:
                        print(f"{child['name']}, {child['age']}")
                else:
                    print(f"User with login: {self.login} has no children.")
        except sqlite3.Error:
            print("Error while getting user's children from database.")

    @authentication_required
    def find_similar_children_by_age(self):
        if self.db_available:
            self.find_similar_children_by_age_db()
        else:
            try:
                children_ages = [
                    child["age"] for child in self.get_children_of_logged_user()
                ]
            except TypeError:
                print(f"User with login: {self.login} has no children.")
            else:
                similar_users = Actions.find_users_with_children_of_age(children_ages)
                try:
                    for user in similar_users:
                        if (
                            user["telephone_number"] == self.login
                            or user["email"] == self.login
                        ):
                            continue
                        children_sorted_by_name = sorted(
                            user["children"], key=lambda x: x["name"]
                        )
                        children_join = "; ".join(
                            f"{child['name']}, {child['age']}"
                            for child in children_sorted_by_name
                        )
                        print(
                            f"{user['firstname']}, {user['telephone_number']}: {children_join}"
                        )
                except IndexError:
                    print("Not found users with children of the same age.")

    @authentication_required
    def find_similar_children_by_age_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                try:
                    ages_of_logged_user_children = [
                        child["age"]
                        for child in self.get_children_of_logged_user_db(cursor)
                    ]
                except TypeError:
                    print(f"User with login: {self.login} has no children.")
                else:
                    placeholders = ",".join("?" * len(ages_of_logged_user_children))
                    cursor.execute(
                        """SELECT DISTINCT parent_id FROM users_children
                            WHERE child_age IN ({});""".format(
                            placeholders
                        ),
                        ages_of_logged_user_children,
                    )
                    users_with_similar_children_age = [
                        user[0] for user in cursor.fetchall()
                    ]
                    for user_id in users_with_similar_children_age:
                        cursor.execute(
                            """SELECT firstname, email,telephone_number FROM users_data
                                    WHERE user_id = ? AND (email !=  ? AND telephone_number != ?);""",
                            (user_id, self.login, self.login),
                        )
                        result = cursor.fetchone()
                        if result:
                            firstname, email, telephone_number = result
                            cursor.execute(
                                """SELECT child_name, child_age FROM users_children WHERE parent_id = ?;""",
                                (user_id,),
                            )
                            children_info = cursor.fetchall()
                            sorted_by_children_name = sorted(
                                children_info, key=lambda x: x[0]
                            )
                            children_join = "; ".join(
                                f"{child[0]}, {child[1]}"
                                for child in sorted_by_children_name
                            )
                            print(f"{firstname}, {telephone_number}: {children_join}")

        except sqlite3.Error:
            print("Error while finding the similar children by age from database.")

    @staticmethod
    def find_users_with_children_of_age(
        list_of_ages: List[int],
    ) -> Optional[List[dict]]:
        def has_matching_child(children):
            return any(
                isinstance(child, dict) and child["age"] in list_of_ages
                for child in children
            )

        users_with_children = final_users_data[final_users_data["children"].notna()]
        users_with_children_of_age = users_with_children[
            users_with_children["children"].apply(has_matching_child)
        ].to_dict(orient="records")
        return users_with_children_of_age

    @admin_required
    def print_all_accounts(self):
        if self.db_available:
            self.print_all_accounts_db()
        else:
            print(len(final_users_data))

    @admin_required
    def print_all_accounts_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("""SELECT COUNT(*) FROM users_data;""")
                all_accounts = cursor.fetchone()
                if all_accounts:
                    print(int(all_accounts[0]))
        except sqlite3.Error:
            print("Error while getting the number of all accounts from database.")

    @admin_required
    def print_oldest_account(self):
        if self.db_available:
            self.print_oldest_account_db()
        else:
            oldest_account = final_users_data.sort_values(by="created_at").to_dict(
                orient="records"
            )[0]
            if oldest_account is not None:
                print(
                    f"name: {oldest_account['firstname']}\n"
                    f"email_address: {oldest_account['email']}\n"
                    f"created_at: {oldest_account['created_at']}"
                )

    @admin_required
    def print_oldest_account_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute(
                    """SELECT firstname, email, created_at FROM users_data ORDER BY created_at ASC LIMIT 1;"""
                )
                firstname, email, created_at = cursor.fetchone()
                print(
                    f"name: {firstname}\n"
                    f"email_address: {email}\n"
                    f"created_at: {created_at}"
                )
        except sqlite3.Error:
            print("Error while getting the oldest account from database.")

    @admin_required
    def group_children_by_age(self):
        if self.db_available:
            self.group_children_by_age_db()
        else:
            children_data = final_users_data["children"].to_list()
            children_valid_data = [
                child for child in children_data if child is not None
            ]
            children_ages = [
                child["age"]
                for user in children_valid_data
                for child in user
                if isinstance(child["age"], int)
            ]
            grouped_ages = Actions.group_children_ages_helper(children_ages)
            for child_age in grouped_ages:
                print(f"age: {child_age['age']}, count: {child_age['count']}")

    @admin_required
    def group_children_by_age_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("""SELECT child_age from users_children""")
                result_ages_of_all_children = cursor.fetchall()
                if result_ages_of_all_children:
                    children_ages = [child[0] for child in result_ages_of_all_children]
                    grouped_ages = Actions.group_children_ages_helper(children_ages)
                    for child_age in grouped_ages:
                        print(f"age: {child_age['age']}, count: {child_age['count']}")
        except sqlite3.Error:
            print("Error while grouping children by age from database.")

    @staticmethod
    def group_children_ages_helper(list_of_children_ages: List[int]) -> List[dict]:
        sorted_list_od_children_ages = sorted(list_of_children_ages)
        grouped_ages_of_children = sorted(
            [
                {"age": key, "count": len(list(group))}
                for key, group in itertools.groupby(sorted_list_od_children_ages)
            ],
            key=lambda x: x["count"],
        )
        return grouped_ages_of_children

    def get_data_of_user(self) -> Optional[dict]:
        try:
            user_data = final_users_data[
                (
                    (final_users_data["email"] == self.login)
                    | (final_users_data["telephone_number"] == self.login)
                )
                & (final_users_data["password"] == self.password)
            ].to_dict(orient="records")[0]
        except (TypeError, IndexError):
            return None
        else:
            return user_data

    def get_children_of_logged_user(self) -> Optional[List[dict]]:
        user_data = self.get_data_of_user()
        if user_data and isinstance(user_data.get("children"), list):
            return user_data["children"]
        return None

    def get_children_of_logged_user_db(self, cursor: Cursor) -> Optional[List[dict]]:
        cursor.execute(
            """SELECT uc.child_name, uc.child_age FROM users_children uc
                            JOIN users_data ud ON uc.parent_id = ud.user_id
                            WHERE ud.email = ? OR ud.telephone_number = ?; """,
            (self.login, self.login),
        )
        result = cursor.fetchall()
        if result:
            children_data = [{"name": child[0], "age": child[1]} for child in result]
        else:
            return None
        return children_data

    def get_role_of_logged_user(self) -> Optional[str]:
        user_data = self.get_data_of_user()
        if user_data and isinstance(user_data.get("role"), str):
            return user_data["role"]
        return None

    def get_role_of_logged_user_db(self, cursor: Cursor) -> Optional[str]:
        cursor.execute(
            "SELECT role FROM users_data WHERE (email = ? OR telephone_number = ?) AND password = ?;",
            (self.login, self.login, self.password),
        )
        user_role = cursor.fetchone()
        if user_role:
            return user_role[0]
        else:
            return None

    @admin_required
    def create_database(self):
        if not self.db_available:
            try:
                with sqlite3.connect(db) as db_conn:
                    cursor = db_conn.cursor()
                    Actions.create_starting_db_tables(cursor)
                    Actions.add_users_data_to_db(db_conn, final_users_data)
                    print("Database created and users data added.")
            except sqlite3.Error:
                print("Error while creating/filling db tables.")
        else:
            print("Database exists already.")

    @staticmethod
    def add_users_data_to_db(db_conn: Connection, users_data: DataFrame):
        cursor = db_conn.cursor()
        try:
            for index, row in users_data.iterrows():
                cursor.execute(
                    """INSERT INTO users_data
                        (email, firstname, telephone_number, password, role, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        row["email"],
                        row["firstname"],
                        row["telephone_number"],
                        row["password"],
                        row["role"],
                        row["created_at"],
                    ),
                )
                user_id = cursor.lastrowid
                if row["children"] is not None:
                    for child in row["children"]:
                        cursor.execute(
                            """INSERT INTO users_children (parent_id, child_name, child_age) VALUES (?, ?, ?)""",
                            (user_id, child["name"], child["age"]),
                        )
                db_conn.commit()
        except sqlite3.Error:
            db_conn.rollback()

    @staticmethod
    def create_starting_db_tables(cursor: Cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_data
              (
                 user_id          INTEGER PRIMARY KEY,
                 email            TEXT NOT NULL,
                 firstname        TEXT NOT NULL,
                 telephone_number TEXT NOT NULL,
                 password         TEXT NOT NULL,
                 role             TEXT NOT NULL,
                 created_at       TEXT NOT NULL,
                 UNIQUE (email, telephone_number)
              )
        ;"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_children
              (
                 parent_id  INTEGER NOT NULL,
                 child_name TEXT NOT NULL,
                 child_age  INTEGER NOT NULL,
                 FOREIGN KEY (parent_id) REFERENCES users_data(user_id) ON DELETE CASCADE
              );"""
        )
