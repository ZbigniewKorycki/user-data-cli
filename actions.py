from users_data_processor import final_users_data
import itertools
import os.path
import sqlite3
import os


class Actions:
    DB_PATH = './users_db.db'

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.authenticated_user = False
        self.role = None
        self.user_data = None
        self.authenticate_user()
        self.db_available = Actions.if_db_available(Actions.DB_PATH)

    def authenticate_user(self):
        try:
            user = final_users_data[
                (
                        (final_users_data["email"] == self.login)
                        | (final_users_data["telephone_number"] == self.login)
                )
                & (final_users_data["password"] == self.password)
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

    @staticmethod
    def if_db_available(db_path) -> bool:
        return True if os.path.exists(db_path) else False

    @authentication_required
    def print_user_children(self):
        if self.db_available:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                children = cursor.execute(
                    "SELECT uc.child_name, uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.email = ? OR ud.telephone_number = ?;",
                    (self.login, self.login)).fetchall()
            except sqlite3.Error as e:
                print("Error while processing db", e)
            else:
                if children:
                    children.sort(key=lambda x: x[0])
                    for child in children:
                        print(f"{child[0]}, {child[1]}")
                else:
                    print(f"User with login: {self.login} has no children.")
            finally:
                db_conn.close()
        else:
            children = self.user_data["children"]
            if children:
                children.sort(key=lambda x: x["name"])
                for child in children:
                    print(f"{child['name']}, {child['age']}")
            else:
                print(f"User with login: {self.login} has no children.")

    @authentication_required
    def find_users_with_similar_children_by_age(self):
        if self.db_available:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                result_user_children = cursor.execute(
                    """SELECT uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.email = ? OR ud.telephone_number = ?;""",
                    (self.login, self.login)).fetchall()
            except sqlite3.Error as e:
                print("Error while processing db", e)
            else:
                user_children_ages = [child[0] for child in result_user_children]
                placeholders = ','.join('?' * len(user_children_ages))
                try:
                    users_with_similar_children_age = cursor.execute(
                        """SELECT DISTINCT parent_id FROM users_children WHERE child_age IN ({});""".format(
                            placeholders),
                        user_children_ages).fetchall()
                except sqlite3.Error as e:
                    print("Error while processing db", e)
                else:
                    users_with_similar_children_age_list = [user[0] for user in users_with_similar_children_age]
                    try:
                        for user_id in users_with_similar_children_age_list:
                            result = cursor.execute(
                                """SELECT ud.firstname, ud.email, ud.telephone_number, uc.child_name, uc.child_age FROM users_children uc JOIN users_data ud ON uc.parent_id = ud.user_id WHERE ud.user_id = ?""",
                                (user_id,)).fetchall()
                            sorted_by_children_name = sorted(result, key=lambda x: x[3])
                            parent_name = sorted_by_children_name[0][0]
                            parent_telephone = sorted_by_children_name[0][2]
                            children_formatted = '; '.join(
                                f"{child[3]}, {child[4]}" for child in sorted_by_children_name)
                            print(f"{parent_name}, {parent_telephone}: {children_formatted}")
                    except sqlite3.Error as e:
                        print("Error while processing db", e)
                    finally:
                        db_conn.close()

        else:
            try:
                user_children_age = [child["age"] for child in self.user_data["children"]]
            except TypeError:
                print(f"User with login: {self.login} has no children. Can not find any matches.")
            else:
                users_with_children = final_users_data[final_users_data["children"].notna()]
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
        if self.db_available:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                result = cursor.execute("""SELECT COUNT(*) FROM users_data;""").fetchone()[0]
                print(int(result))
            except sqlite3.Error as e:
                print("Error while processing db", e)
            finally:
                db_conn.close()
        else:
            print(len(final_users_data))

    @admin_required
    def print_oldest_account(self):
        if self.db_available:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                firstname, email, created_at = cursor.execute(
                    """SELECT firstname, email, created_at FROM users_data ORDER BY created_at ASC LIMIT 1;""").fetchone()
                print(
                    f"name: {firstname}\n"
                    f"email_address: {email}\n"
                    f"created_at: {created_at}"
                )
            except sqlite3.Error as e:
                print("Error while processing db", e)
            finally:
                db_conn.close()
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
    def group_children_by_age(self):
        if self.db_available:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                result = cursor.execute("""SELECT child_age from users_children""").fetchall()
            except sqlite3.Error as e:
                print("Error while processing db", e)
            else:
                children_ages = [child[0] for child in result]
            finally:
                db_conn.close()
        else:
            children_data = final_users_data["children"].to_list()
            filtered_children_without_none = [
                child for child in children_data if child is not None
            ]
            children_ages = []
            for user_children in filtered_children_without_none:
                for child in user_children:
                    if isinstance(child["age"], int):
                        children_ages.append(child["age"])

        sorted_children_ages = sorted(children_ages)
        grouped_children_ages = sorted(
            [
                {"age": key, "count": len(list(group))}
                for key, group in itertools.groupby(sorted_children_ages)
            ],
            key=lambda x: x["count"],
        )
        for child_age in grouped_children_ages:
            print(f"age: {child_age['age']}, count: {child_age['count']}")

    @admin_required
    def create_database(self):
        if self.db_available:
            print("Database exists already.")
        else:
            db_conn = sqlite3.connect(Actions.DB_PATH)
            cursor = db_conn.cursor()
            try:
                Actions.create_starting_db_tables(cursor)
                Actions.add_users_data_to_db(db_conn, final_users_data)
            except sqlite3.Error as e:
                print("Error while creating/filling db tables:", e)
            else:
                print("Database created and users data added.")
            finally:
                db_conn.close()

    @staticmethod
    def add_users_data_to_db(db_conn, users_data):
        cursor = db_conn.cursor()
        try:
            for index, row in users_data.iterrows():
                cursor.execute(
                    "INSERT INTO users_data (email, firstname, telephone_number, password, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (row['email'], row['firstname'], row['telephone_number'], row['password'], row['role'],
                     row['created_at']))
                user_id = cursor.lastrowid
                if row["children"] is not None:
                    for child in row["children"]:
                        cursor.execute(
                            "INSERT INTO users_children (parent_id, child_name, child_age) VALUES (?, ?, ?)",
                            (user_id, child['name'], child['age'])
                        )
                db_conn.commit()
        except sqlite3.Error as e:
            print("Error while filling in db tables:", e)
            db_conn.rollback()
        finally:
            db_conn.close()

    @staticmethod
    def create_starting_db_tables(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS users_data (
            user_id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            firstname TEXT NOT NULL,
            telephone_number TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (email, telephone_number)
        );""")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_children (
            parent_id INTEGER NOT NULL,
            child_name TEXT NOT NULL,
            child_age INTEGER NOT NULL,
            FOREIGN KEY (parent_id)
                REFERENCES users_data(user_id)
                ON DELETE CASCADE
        );""")
