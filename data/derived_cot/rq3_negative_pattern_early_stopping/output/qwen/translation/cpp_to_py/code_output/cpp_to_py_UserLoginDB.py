import sqlite3
from typing import Tuple, Optional

class UserLoginDB:
    def __init__(self, db_name: str):
        self._conn = None
        self._cursor = None
        try:
            self._conn = sqlite3.connect(db_name)
            self._cursor = self._conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {str(e)}") from e

    def __del__(self):
        self.close()

    def insert_user(self, username: str, password: str) -> None:
        try:
            self._cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            # No need to commit as SQLite changes are immediate unless a transaction is started
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {str(e)}") from e

    def search_user_by_username(self, username: str) -> Optional[Tuple[str, str]]:
        try:
            self._cursor.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (username,)
            )
            row = self._cursor.fetchone()
            if row:
                return (row[0], row[1])
            return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to search user: {str(e)}") from e

    def delete_user_by_username(self, username: str) -> None:
        try:
            self._cursor.execute(
                "DELETE FROM users WHERE username = ?",
                (username,)
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {str(e)}") from e

    def validate_user_login(self, username: str, password: str) -> bool:
        user = self.search_user_by_username(username)
        if user and user[1] == password:
            return True
        return False

    def create_table(self) -> None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
        """
        try:
            self._cursor.execute(create_table_query)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {str(e)}") from e

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
            self._cursor = None