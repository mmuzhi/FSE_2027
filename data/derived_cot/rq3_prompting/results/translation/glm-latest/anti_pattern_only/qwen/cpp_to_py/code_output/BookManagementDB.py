import sqlite3


class BookManagementDB:
    def __init__(self, db_name: str) -> None:
        self.connection = None
        try:
            # isolation_level=None -> autocommit mode, matching the C++ code's
            # use of sqlite3_exec / sqlite3_step without explicit transactions.
            self.connection = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def __del__(self) -> None:
        # Mirrors the C++ destructor: close the connection, ignoring errors.
        connection = getattr(self, "connection", None)
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass

    def create_table(self) -> None:
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

    def add_book(self, title: str, author: str) -> None:
        insert_sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        try:
            self.connection.execute(insert_sql, (title, author))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def remove_book(self, id: int) -> None:
        delete_sql = "DELETE FROM books WHERE id = ?"
        try:
            self.connection.execute(delete_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def borrow_book(self, id: int) -> None:
        update_sql = "UPDATE books SET available = 0 WHERE id = ?"
        try:
            self.connection.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def return_book(self, id: int) -> None:
        update_sql = "UPDATE books SET available = 1 WHERE id = ?"
        try:
            self.connection.execute(update_sql, (id,))
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

    def search_books(self) -> list[tuple[int, str, str, int]]:
        select_sql = "SELECT * FROM books"
        books = []

        try:
            cursor = self.connection.execute(select_sql)
        except sqlite3.Error as e:
            raise RuntimeError(str(e))

        try:
            # Mirrors `while (sqlite3_step(stmt) == SQLITE_ROW)`: if stepping
            # fails mid-way, stop silently and return the rows gathered so far.
            for row in cursor:
                books.append((row[0], row[1], row[2], row[3]))
        except sqlite3.Error:
            pass

        return books

    def get_connection(self) -> sqlite3.Connection:
        return self.connection