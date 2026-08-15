import sqlite3


class UserLoginDB:
    def __init__(self, db_name: str):
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {e}")
        self.create_table()

    def __del__(self):
        try:
            self.close_connection()
        except Exception:
            pass

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_table(self):
        if self.connection is None:
            raise RuntimeError("Cannot create table: not connected")
        try:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {e}")

    def insert_user(self, username: str, password: str):
        if self.connection is None:
            raise RuntimeError("Failed to prepare statement: not connected")
        try:
            self.connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {e}")

    def search_user_by_username(self, username: str):
        if self.connection is None:
            raise RuntimeError("Failed to prepare statement: not connected")
        try:
            cur = self.connection.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (username,),
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to prepare statement: {e}")

        try:
            row = cur.fetchone()
        except sqlite3.Error:
            return None

        if row is not None:
            return (row[0], row[1])
        return None

    def delete_user_by_username(self, username: str):
        if self.connection is None:
            raise RuntimeError("Failed to prepare statement: not connected")
        try:
            self.connection.execute(
                "DELETE FROM users WHERE username = ?",
                (username,),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {e}")

    def validate_user_login(self, username: str, password: str) -> bool:
        user = self.search_user_by_username(username)
        if user and user[1] == password:
            return True
        return False