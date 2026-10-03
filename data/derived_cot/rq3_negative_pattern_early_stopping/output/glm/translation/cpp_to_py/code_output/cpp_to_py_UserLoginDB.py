import sqlite3
from typing import Optional, Tuple

class UserLoginDB:
    def __init__(self, db_name: str) -> None:
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        try:
            self.connection = sqlite3.connect(db_name, isolation_level=None, timeout=0)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {e}")
        self.create_table()

    def __del__(self) -> None:
        self.close_connection()

    def insert_user(self, username: str, password: str) -> None:
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {e}")

    def search_user_by_username(self, username: str) -> Optional[Tuple[str, str]]:
        try:
            self.cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to prepare statement: {e}")
        
        try:
            row = self.cursor.fetchone()
        except sqlite3.Error:
            return None

        if row:
            return (row[0], row[1])
        return None

    def delete_user_by_username(self, username: str) -> None:
        try:
            self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {e}")

    def validate_user_login(self, username: str, password: str) -> bool:
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
            )
        """
        try:
            self.cursor.execute(create_table_query)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {e}")