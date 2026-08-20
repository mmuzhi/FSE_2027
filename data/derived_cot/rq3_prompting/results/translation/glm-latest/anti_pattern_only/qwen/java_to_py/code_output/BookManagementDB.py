import sqlite3


class Book:
    """Python equivalent of the Java static nested class BookManagementDB.Book."""

    def __init__(self, id, title, author, available):
        self.id = id
        self.title = title
        self.author = author
        self.available = available

    def __str__(self):
        # Java string concatenation renders null as "null"
        title = "null" if self.title is None else self.title
        author = "null" if self.author is None else self.author
        return (f"Book{{id={self.id}, title='{title}', "
                f"author='{author}', available={self.available}}}")

    # Alias so containers (e.g. printing a list) render like Java's toString()
    __repr__ = __str__


class BookManagementDB:
    def __init__(self, db_name):
        # isolation_level=None enables autocommit, matching JDBC's default
        # (java.sql.Connection autocommit == true), so every statement is
        # committed on execution exactly like the Java version.
        self.connection = sqlite3.connect(db_name, isolation_level=None)
        # Name-based row access, mirroring ResultSet.getXxx("column")
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")"
        )
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
        for row in self.connection.execute(select_sql):
            available = row["available"]
            if available is None:
                # JDBC ResultSet.getInt() returns 0 for SQL NULL
                available = 0
            books.append(Book(row["id"], row["title"], row["author"], available))
        return books