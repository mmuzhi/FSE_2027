import sqlite3


class BookManagementDB:
    class Book:
        def __init__(self, id, title, author, available):
            self.id = id
            self.title = title
            self.author = author
            self.available = available

        def getId(self):
            return self.id

        def getTitle(self):
            return self.title

        def getAuthor(self):
            return self.author

        def getAvailable(self):
            return self.available

        def __repr__(self):
            return f"Book{{id={self.id}, title='{self.title}', author='{self.author}', available={self.available}}}"

        __str__ = __repr__

    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        self.connection.isolation_level = None  # autocommit mode, like Java's default
        self.createTable()

    def createTable(self):
        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")"
        )
        self.connection.execute(create_table_sql)

    def addBook(self, title, author):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        self.connection.execute(insert_sql, (title, author))

    def removeBook(self, bookId):
        delete_sql = "DELETE FROM books WHERE id = ?"
        self.connection.execute(delete_sql, (bookId,))

    def borrowBook(self, bookId):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        self.connection.execute(update_sql, (bookId,))

    def returnBook(self, bookId):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        self.connection.execute(update_sql, (bookId,))

    def searchBooks(self):
        select_sql = "SELECT * FROM books"
        cursor = self.connection.execute(select_sql)
        books = []
        for row in cursor.fetchall():
            id, title, author, available = row
            books.append(BookManagementDB.Book(id, title, author, available))
        return books