import sqlite3
from typing import List, Tuple

class BookManagementDB:
    def __init__(self, db_name: str):
        try:
            self.connection = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER NOT NULL
            )
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def add_book(self, title: str, author: str):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_sql, (title, author))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def remove_book(self, id: int):
        delete_sql = "DELETE FROM books WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(delete_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def borrow_book(self, id: int):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def return_book(self, id: int):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def search_books(self) -> List[Tuple[int, str, str, int]]:
        select_sql = "SELECT * FROM books"
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_sql)
        except sqlite3.Error as e:
            raise RuntimeError(str(e))
        return cursor.fetchall()

    def get_connection(self):
        return self.connection