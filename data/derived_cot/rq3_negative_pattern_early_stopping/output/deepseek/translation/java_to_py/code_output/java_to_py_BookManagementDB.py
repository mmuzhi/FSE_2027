import sqlite3

class BookManagementDB:
    class Book:
        def __init__(self, id: int, title: str, author: str, available: int):
            self.id = id
            self.title = title
            self.author = author
            self.available = available

        def getId(self) -> int:
            return self.id

        def getTitle(self) -> str:
            return self.title

        def getAuthor(self) -> str:
            return self.author

        def getAvailable(self) -> int:
            return self.available

        def __str__(self) -> str:
            return (
                f"Book{{id={self.id}, title='{self.title}', "
                f"author='{self.author}', available={self.available}}}"
            )

    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
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
        with self.connection:
            self.connection.execute(create_table_sql)

    def addBook(self, title: str, author: str):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        with self.connection:
            self.connection.execute(insert_sql, (title, author))

    def removeBook(self, bookId: int):
        delete_sql = "DELETE FROM books WHERE id = ?"
        with self.connection:
            self.connection.execute(delete_sql, (bookId,))

    def borrowBook(self, bookId: int):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        with self.connection:
            self.connection.execute(update_sql, (bookId,))

    def returnBook(self, bookId: int):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        with self.connection:
            self.connection.execute(update_sql, (bookId,))

    def searchBooks(self):
        select_sql = "SELECT * FROM books"
        rows = self.connection.execute(select_sql).fetchall()
        books = []
        for row in rows:
            id_, title, author, available = row
            books.append(self.Book(id_, title, author, available))
        return books