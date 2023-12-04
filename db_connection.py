import sqlite3
from sqlite3 import Error
from config import sqlite_config


class SQLiteConnection:

    def __init__(self, db_file=sqlite_config.db_file):
        self.db_file = db_file

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error: {e}")
            return None

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
                else:
                    return None
            except Error as e:
                print("Error executing query:", e)
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")
