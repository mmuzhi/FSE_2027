import sqlite3
import traceback

class UserLoginDB:
    def __init__(self, dbName):
        self.connection = None
        try:
            if dbName is None:
                dbName = "null"
            self.connection = sqlite3.connect(dbName)
            self.connection.isolation_level = None
            self.connection.row_factory = sqlite3.Row
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

    def insertUser(self, username, password):
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (username, password))
        except sqlite3.Error:
            traceback.print_exc()

    def searchUserByUsername(self, username):
        search_query = "SELECT * FROM users WHERE username = ?"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(search_query, (username,))
                row = cursor.fetchone()
                if row:
                    username_val = row['username']
                    password_val = row['password']
                    return f"{'null' if username_val is None else username_val},{'null' if password_val is None else password_val}"
        except (sqlite3.Error, IndexError):
            traceback.print_exc()
        return None

    def deleteUserByUsername(self, username):
        delete_query = "DELETE FROM users WHERE username = ?"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(delete_query, (username,))
        except sqlite3.Error:
            traceback.print_exc()

    def validateUserLogin(self, username, password):
        user = self.searchUserByUsername(username)
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