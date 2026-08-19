import sqlite3
import traceback


def _jstr(value):
    # Mimics Java string concatenation, where a null reference renders as "null".
    return "null" if value is None else value


def _jsplit(s, sep=","):
    # Mimics Java's String.split, which discards trailing empty strings.
    parts = s.split(sep)
    while len(parts) > 1 and parts[-1] == "":
        parts.pop()
    return parts


class UserLoginDB:
    def __init__(self, db_name):
        self.connection = None
        try:
            # isolation_level=None -> autocommit, matching JDBC's default autoCommit=true
            self.connection = sqlite3.connect(db_name, isolation_level=None)
            self.createTable()
        except sqlite3.Error:
            traceback.print_exc()

    def createTable(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
        cur = None
        try:
            cur = self.connection.cursor()
            cur.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if cur is not None:
                cur.close()

    def insertUser(self, username, password):
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cur = None
        try:
            cur = self.connection.cursor()
            cur.execute(insert_query, (username, password))
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if cur is not None:
                cur.close()

    def searchUserByUsername(self, username):
        search_query = "SELECT * FROM users WHERE username = ?"
        cur = None
        try:
            cur = self.connection.cursor()
            cur.execute(search_query, (username,))
            row = cur.fetchone()
            if row is not None:
                return _jstr(row[0]) + "," + _jstr(row[1])
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if cur is not None:
                cur.close()
        return None

    def deleteUserByUsername(self, username):
        delete_query = "DELETE FROM users WHERE username = ?"
        cur = None
        try:
            cur = self.connection.cursor()
            cur.execute(delete_query, (username,))
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if cur is not None:
                cur.close()

    def validateUserLogin(self, username, password):
        user = self.searchUserByUsername(username)
        if user is not None:
            parts = _jsplit(user)
            return parts[1] == password
        return False

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except sqlite3.Error:
            traceback.print_exc()