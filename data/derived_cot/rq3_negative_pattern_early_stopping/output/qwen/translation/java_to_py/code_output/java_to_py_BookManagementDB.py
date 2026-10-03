import sqlite3
from typing import List

class BookManagementDB:

    class Book:
        def __init__(self, id: int, title: str, author: str, available: int):
            self.id = id
            self.title = title
            self.author = author
            self.available = available

        def __repr__(self):
            return f"Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.available})"

    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            available INTEGER
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(create_table_sql)
        self.connection.commit()

    def add_book(self, title: str, author: str):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        cursor = self.connection.cursor()
        cursor.execute(insert_sql, (title, author))
        self.connection.commit()

    def remove_book(self, book_id: int):
        delete_sql = "DELETE FROM books WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(delete_sql, (book_id,))
        self.connection.commit()

    def borrow_book(self, book_id: int):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(update_sql, (book_id,))
        self.connection.commit()

    def return_book(self, book_id: int):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(update_sql, (book_id,))
        self.connection.commit()

    def search_books(self) -> List['BookManagementDB.Book']:
        select_sql = "SELECT * FROM books"
        cursor = self.connection.cursor()
        cursor.execute(select_sql)
        books = []
        for row in cursor.fetchall():
            book = self.Book(row[0], row[1], row[2], row[3])
            books.append(book)
        return books

# Example usage (if needed)
if __name__ == "__main__":
    try:
        db = BookManagementDB("books.db")
        db.add_book("Python Crash Course", "Eric Matthes")
        db.add_book("The Python Bible", "John Doe")
        for book in db.search_books():
            print(book)
        db.borrow_book(1)
        for book in db.search_books():
            print(book)
        db.return_book(1)
        for book in db.search_books():
            print(book)
        db.remove_book(2)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection if needed (but the __del__ method of sqlite3.Connection might handle it)
        # However, we don't have a close method in our class. We can add one if needed.
        pass