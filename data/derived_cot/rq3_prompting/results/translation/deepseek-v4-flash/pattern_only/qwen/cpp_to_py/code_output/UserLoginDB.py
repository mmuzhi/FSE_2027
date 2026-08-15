import sqlite3

class UserLoginDB:
    def __init__(self, db_name):
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name)
            self.connection.isolation_level = None
        except sqlite3.Error as e:
            raise RuntimeError("Cannot open database: " + str(e))
        self.create_table()

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    @staticmethod
    def _truncate(s):
        if s is None:
            return None
        return s.split('\x00', 1)[0]

    def _check_connection(self):
        if self.connection is None:
            raise RuntimeError("Failed to prepare statement: bad parameter or other API misuse")

    def insert_user(self, username, password):
        self._check_connection()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (self._truncate(username), self._truncate(password))
            )
        except sqlite3.Error as e:
            raise RuntimeError("Failed to insert user: " + str(e))
        finally:
            cursor.close()

    def search_user_by_username(self, username):
        self._check_connection()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (self._truncate(username),)
            )
            row = cursor.fetchone()
        except sqlite3.Error:
            return None
        finally:
            cursor.close()
        if row is not None:
            return (self._truncate(row[0]), self._truncate(row[1]))
        return None

    def delete_user_by_username(self, username):
        self._check_connection()
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM users WHERE username = ?",
                (self._truncate(username),)
            )
        except sqlite3.Error as e:
            raise RuntimeError("Failed to delete user: " + str(e))
        finally:
            cursor.close()

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

    def create_table(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        except sqlite3.Error as e:
            raise RuntimeError("Cannot create table: " + str(e))
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None