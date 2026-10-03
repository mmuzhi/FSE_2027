import sqlite3


class BookManagementDB:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, isolation_level=None)
        self._create_table()

    def _create_table(self):
        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")"
        )
        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_sql)
        finally:
            cursor.close()

    def add_book(self, title, author):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_sql, (title, author))
        finally:
            cursor.close()

    def remove_book(self, book_id):
        delete_sql = "DELETE FROM books WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(delete_sql, (book_id,))
        finally:
            cursor.close()

    def borrow_book(self, book_id):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_sql, (book_id,))
        finally:
            cursor.close()

    def return_book(self, book_id):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_sql, (book_id,))
        finally:
            cursor.close()

    def search_books(self):
        select_sql = "SELECT * FROM books"
        books = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_sql)
            for row in cursor.fetchall():
                books.append(Book(row[0], row[1], row[2], row[3]))
        finally:
            cursor.close()
        return books


class Book:

    def __init__(self, id, title, author, available):
        self.id = id
        self.title = title
        self.author = author
        self.available = available

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_available(self):
        return self.available

    def __str__(self):
        return (
            f"Book{{id={self.id}, title='{self.title}', "
            f"author='{self.author}', available={self.available}}}"
        )