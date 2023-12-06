from users_data_processor import final_users_data
from config.db_config import db
import itertools
import os.path
import sqlite3
import os
from typing import Optional, List


class Actions:
    def __init__(self, login, password):
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
            if user is not None:
                self.authenticated_user = True
                self.role = self.get_data_of_user_role()

    def authenticate_user_with_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute(
                    "SELECT role FROM users_data WHERE (email = ? OR telephone_number = ?) AND password = ?;",
                    (self.login, self.login, self.password),
                )
                user_role = cursor.fetchone()
                if user_role:
                    self.authenticated_user = True
                    self.role = user_role[0]
        except sqlite3.Error as e:
            print("Error while processing db", e)

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
    def is_db_available(db_path) -> bool:
        return True if os.path.exists(db_path) else False

    @authentication_required
    def print_children(self):
        if self.db_available:
            self.print_children_db()
        else:
            user_children = self.get_data_of_user_children()
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
                cursor.execute(
                    "SELECT uc.child_name, uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.email = ? OR ud.telephone_number = ?;",
                    (self.login, self.login),
                )
                children_of_user = cursor.fetchall()
                if children_of_user:
                    children_of_user.sort(key=lambda x: x[0])
                    for child in children_of_user:
                        print(f"{child[0]}, {child[1]}")
                else:
                    print(f"User with login: {self.login} has no children.")
        except sqlite3.Error as e:
            print("Error while processing db", e)

    @authentication_required
    def find_similar_children_by_age(self):
        if self.db_available:
            self.find_similar_children_by_age_db()
        else:
            try:
                users_children_data = self.get_data_of_user_children()
                ages_of_users_children = [child["age"] for child in users_children_data]
            except TypeError:
                print(f"User with login: {self.login} has no children.")
            else:
                users_with_children = final_users_data[
                    final_users_data["children"].notna()
                ]
                users_with_children_of_similar_age = users_with_children[
                    users_with_children["children"].apply(
                        lambda x: (
                            any(
                                child["age"] in ages_of_users_children
                                for child in x
                                if isinstance(child, dict)
                            )
                        )
                    )
                ]
                similar_users = users_with_children_of_similar_age.to_dict(
                    orient="records"
                )
                for user in similar_users:
                    if (
                        user["telephone_number"] == self.login
                        or user["email"] == self.login
                    ):
                        continue
                    children_sorted_by_name = sorted(
                        user["children"], key=lambda x: x["name"]
                    )
                    all_children_info = "; ".join(
                        f"{child['name']}, {child['age']}"
                        for child in children_sorted_by_name
                    )
                    print(
                        f"{user['firstname']}, {user['telephone_number']}: {all_children_info}"
                    )

    @authentication_required
    def find_similar_children_by_age_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute(
                    """SELECT uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.email = ? OR ud.telephone_number = ?;""",
                    (self.login, self.login),
                )
                result_user_children = cursor.fetchall()
                ages_of_users_children = [child[0] for child in result_user_children]
                placeholders = ",".join("?" * len(ages_of_users_children))
                cursor.execute(
                    """SELECT DISTINCT parent_id FROM users_children WHERE child_age IN ({});""".format(
                        placeholders
                    ),
                    ages_of_users_children,
                )
                users_with_similar_children_age = cursor.fetchall()
                users_with_similar_children_age_list = [
                    user[0] for user in users_with_similar_children_age
                ]
                for user_id in users_with_similar_children_age_list:
                    cursor.execute(
                        """SELECT ud.firstname, ud.email, ud.telephone_number, uc.child_name, uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.user_id = ?""",
                        (user_id,),
                    )
                    result = cursor.fetchall()
                    sorted_by_children_name = sorted(result, key=lambda x: x[3])
                    parent_name = sorted_by_children_name[0][0]
                    parent_telephone = sorted_by_children_name[0][2]
                    children_formatted = "; ".join(
                        f"{child[3]}, {child[4]}" for child in sorted_by_children_name
                    )
                    print(f"{parent_name}, {parent_telephone}: {children_formatted}")

        except sqlite3.Error as e:
            print("Error while processing db", e)

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
        except sqlite3.Error as e:
            print("Error while processing db", e)

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
                    """SELECT firstname, email, created_at
                     FROM users_data
                    ORDER BY created_at ASC
                    LIMIT 1;"""
                )
                firstname, email, created_at = cursor.fetchone()
                print(
                    f"name: {firstname}\n"
                    f"email_address: {email}\n"
                    f"created_at: {created_at}"
                )
        except sqlite3.Error as e:
            print("Error while processing db", e)

    @admin_required
    def group_children_by_age(self):
        if self.db_available:
            self.group_children_by_age_db()
        else:
            children_data = final_users_data["children"].to_list()
            verified_children_data = [
                child for child in children_data if child is not None
            ]
            ages_of_all_children = [
                child["age"]
                for user in verified_children_data
                for child in user
                if isinstance(child["age"], int)
            ]

            sorted_age_of_children = sorted(ages_of_all_children)
            grouped_age_of_children = sorted(
                [
                    {"age": key, "count": len(list(group))}
                    for key, group in itertools.groupby(sorted_age_of_children)
                ],
                key=lambda x: x["count"],
            )
            for child_age in grouped_age_of_children:
                print(f"age: {child_age['age']}, count: {child_age['count']}")

    @admin_required
    def group_children_by_age_db(self):
        try:
            with sqlite3.connect(db) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("""SELECT child_age from users_children""")
                result_ages_of_all_children = cursor.fetchall()
                if result_ages_of_all_children:
                    ages_of_all_children = [
                        child[0] for child in result_ages_of_all_children
                    ]
                    sorted_age_of_children = sorted(ages_of_all_children)
                    grouped_age_of_children = sorted(
                        [
                            {"age": key, "count": len(list(group))}
                            for key, group in itertools.groupby(sorted_age_of_children)
                        ],
                        key=lambda x: x["count"],
                    )
                    for child_age in grouped_age_of_children:
                        print(f"age: {child_age['age']}, count: {child_age['count']}")
        except sqlite3.Error as e:
            print("Error while processing db", e)

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

    def get_data_of_user_children(self) -> Optional[List[dict]]:
        try:
            children_data = self.get_data_of_user()["children"]
        except TypeError:
            return None
        else:
            return children_data

    def get_data_of_user_role(self) -> Optional[str]:
        try:
            role = self.get_data_of_user()["role"]
        except TypeError:
            return None
        else:
            return role

    @admin_required
    def create_database(self):
        if not self.db_available:
            try:
                with sqlite3.connect(db) as db_conn:
                    cursor = db_conn.cursor()
                    Actions.create_starting_db_tables(cursor)
                    Actions.add_users_data_to_db(db_conn, final_users_data)
                    print("Database created and users data added.")
            except sqlite3.Error as e:
                print("Error while creating/filling db tables:", e)
        else:
            print("Database exists already.")

    @staticmethod
    def add_users_data_to_db(db_conn, users_data):
        cursor = db_conn.cursor()
        try:
            for index, row in users_data.iterrows():
                cursor.execute(
                    "INSERT INTO users_data"
                    "(email, firstname, telephone_number, password, role, created_at)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
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
                            "INSERT INTO users_children"
                            "(parent_id, child_name, child_age)"
                            "VALUES (?, ?, ?)",
                            (user_id, child["name"], child["age"]),
                        )
                db_conn.commit()
        except sqlite3.Error as e:
            print("Error while filling in db tables:", e)
            db_conn.rollback()

    @staticmethod
    def create_starting_db_tables(cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_data (
            user_id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            firstname TEXT NOT NULL,
            telephone_number TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (email, telephone_number)
        );"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_children (
            parent_id INTEGER NOT NULL,
            child_name TEXT NOT NULL,
            child_age INTEGER NOT NULL,
            FOREIGN KEY (parent_id)
                REFERENCES users_data(user_id)
                ON DELETE CASCADE
        );"""
        )
