import sqlite3


class BookManagementDB:

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
            return ("Book{"
                    "id=" + str(self.id) +
                    ", title='" + self.title + "'" +
                    ", author='" + self.author + "'" +
                    ", available=" + str(self.available) +
                    "}")

        __repr__ = __str__

    def __init__(self, db_name):
        # isolation_level=None -> autocommit, matching JDBC default behavior
        self.connection = sqlite3.connect(db_name, isolation_level=None)
        self.create_table()

    def create_table(self):
        create_table_sql = ("CREATE TABLE IF NOT EXISTS books ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "title TEXT, "
                            "author TEXT, "
                            "available INTEGER"
                            ")")
        self.connection.execute(create_table_sql)

    def add_book(self, title, author):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        self.connection.execute(insert_sql, (title, author))

    def remove_book(self, book_id):
        delete_sql = "DELETE FROM books WHERE id = ?"
        self.connection.execute(delete_sql, (book_id,))

    def borrow_book(self, book_id):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        self.connection.execute(update_sql, (book_id,))

    def return_book(self, book_id):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        self.connection.execute(update_sql, (book_id,))

    def search_books(self):
        select_sql = "SELECT * FROM books"
        books = []
        cursor = self.connection.execute(select_sql)
        for row in cursor:
            book_id, title, author, available = row
            books.append(self.Book(book_id, title, author, available))
        return books