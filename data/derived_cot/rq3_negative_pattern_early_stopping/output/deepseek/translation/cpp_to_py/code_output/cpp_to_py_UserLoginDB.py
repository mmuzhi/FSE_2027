import sqlite3
from typing import Optional, Tuple

class UserLoginDB:
    def __init__(self, db_name: str):
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {str(e)}") from e
        self.create_table()

    def __del__(self):
        self.close_connection()

    def create_table(self):
        query = (
            "CREATE TABLE IF NOT EXISTS users ("
            "    username TEXT,"
            "    password TEXT"
            ")"
        )
        try:
            self.connection.execute(query)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {str(e)}") from e

    def insert_user(self, username: str, password: str):
        try:
            self.connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {str(e)}") from e

    def search_user_by_username(self, username: str) -> Optional[Tuple[str, str]]:
        cursor = None
        try:
            cursor = self.connection.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return (row[0], row[1])
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to search user: {str(e)}") from e
        finally:
            if cursor is not None:
                cursor.close()

    def delete_user_by_username(self, username: str):
        try:
            self.connection.execute(
                "DELETE FROM users WHERE username = ?",
                (username,)
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {str(e)}") from e

    def validate_user_login(self, username: str, password: str) -> bool:
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None