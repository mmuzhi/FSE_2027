import sqlite3
from typing import List, Tuple

class BookManagementDB:
    def __init__(self, db_name: str):
        try:
            self.connection = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def __del__(self):
        self.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_table(self):
        sql = (
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "author TEXT NOT NULL, "
            "available INTEGER NOT NULL"
            ")"
        )
        try:
            self.connection.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def add_book(self, title: str, author: str):
        sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        try:
            self.connection.execute(sql, (title, author))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def remove_book(self, id: int):
        sql = "DELETE FROM books WHERE id = ?"
        try:
            self.connection.execute(sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def borrow_book(self, id: int):
        sql = "UPDATE books SET available = 0 WHERE id = ?"
        try:
            self.connection.execute(sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def return_book(self, id: int):
        sql = "UPDATE books SET available = 1 WHERE id = ?"
        try:
            self.connection.execute(sql, (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def search_books(self) -> List[Tuple[int, str, str, int]]:
        sql = "SELECT * FROM books"
        try:
            cursor = self.connection.execute(sql)
            rows = cursor.fetchall()
            books = [(row[0], row[1], row[2], row[3]) for row in rows]
            return books
        except sqlite3.Error as e:
            raise RuntimeError(str(e)) from e

    def get_connection(self):
        return self.connection