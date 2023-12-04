import sqlite3
from sqlite3 import Error


class SQLiteConnection:

    def __init__(self, db_file):
        self.db_file = db_file
        self.create_starting_table()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error: {e}")
            return None

    def create_starting_table(self):
        self.execute_query("""CREATE TABLE IF NOT EXISTS users_data (
            email TEXT PRIMARY KEY,
            firstname TEXT NOT NULL,
            telephone_number TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (email, telephone_number)
        );""")

        self.execute_query(
            """CREATE TABLE IF NOT EXISTS users_children (
            parent_email TEXT NOT NULL,
            child_name TEXT NOT NULL,
            child_age INTEGER NOT NULL,
            FOREIGN KEY (parent_email)
                REFERENCES users_data(email)
                ON DELETE CASCADE
        );""")

    def execute_query(self, query, params=None, fetch_option=None):
        connection = self.create_connection()
        cursor = connection.cursor()
        if connection is not None:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
                if fetch_option == "fetchone":
                    return cursor.fetchone()
                elif fetch_option == "fetchall":
                    return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")
