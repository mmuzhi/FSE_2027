import sqlite3
from typing import List, Tuple

class BookManagementDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name, check_same_thread=False)
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to open database: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection is not None:
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
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")

    def add_book(self, title: str, author: str):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, (title, author))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to add book: {e}")

    def remove_book(self, id: int):
        delete_sql = "DELETE FROM books WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to remove book: {e}")

    def borrow_book(self, id: int):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to borrow book: {e}")

    def return_book(self, id: int):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to return book: {e}")

    def search_books(self) -> List[Tuple[int, str, str, int]]:
        select_sql = "SELECT * FROM books"
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_sql)
            books = []
            for row in cursor.fetchall():
                books.append((row[0], row[1], row[2], row[3]))
            return books
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to search books: {e}")

    def get_connection(self) -> sqlite3.Connection:
        return self.connection