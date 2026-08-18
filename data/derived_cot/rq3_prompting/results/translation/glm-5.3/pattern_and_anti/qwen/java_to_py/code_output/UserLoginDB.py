import sqlite3
import traceback


class UserLoginDB:
    def __init__(self, db_name):
        try:
            # isolation_level=None => autocommit, matching JDBC default behavior
            self.connection = sqlite3.connect(db_name, isolation_level=None)
            self._create_table()
        except sqlite3.Error:
            traceback.print_exc()

    def _create_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()

    def insert_user(self, username, password):
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (username, password))
        except sqlite3.Error:
            traceback.print_exc()

    def search_user_by_username(self, username):
        search_query = "SELECT * FROM users WHERE username = ?"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(search_query, (username,))
                row = cursor.fetchone()
                if row is not None:
                    return row[0] + "," + row[1]
        except sqlite3.Error:
            traceback.print_exc()
        return None

    def delete_user_by_username(self, username):
        delete_query = "DELETE FROM users WHERE username = ?"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(delete_query, (username,))
        except sqlite3.Error:
            traceback.print_exc()

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None:
            parts = user.split(",")
            return parts[1] == password
        return False

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except sqlite3.Error:
            traceback.print_exc()