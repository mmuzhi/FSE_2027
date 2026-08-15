import sqlite3


class BookManagementDB:
    def __init__(self, db_name):
        self.connection = None
        try:
            # isolation_level=None makes each statement autocommit, matching raw sqlite3 behavior
            self.connection = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def __del__(self):
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
            self.connection.execute(create_table_sql)
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def add_book(self, title, author):
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        # Mimic C++ sqlite3_bind_text(..., -1, SQLITE_TRANSIENT): truncate at first NUL
        title = title.split('\0', 1)[0]
        author = author.split('\0', 1)[0]
        try:
            self.connection.execute(insert_sql, (title, author))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def remove_book(self, id):
        delete_sql = "DELETE FROM books WHERE id = ?"
        try:
            self.connection.execute(delete_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def borrow_book(self, id):
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        try:
            self.connection.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def return_book(self, id):
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        try:
            self.connection.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def search_books(self):
        select_sql = "SELECT * FROM books"
        try:
            cursor = self.connection.execute(select_sql)
            books = []
            for row in cursor.fetchall():
                id, title, author, available = row
                # Mimic std::string from sqlite3_column_text (NUL-terminated)
                title = title.split('\0', 1)[0]
                author = author.split('\0', 1)[0]
                books.append((id, title, author, available))
            return books
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def get_connection(self):
        return self.connection