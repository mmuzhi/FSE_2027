import sqlite3


class UserLoginDB:
    def __init__(self, db_name):
        self.connection = None
        self.stmt = None
        self.query = None
        try:
            # isolation_level=None keeps sqlite in autocommit mode,
            # matching the default sqlite3_open behavior in the C++ version.
            self.connection = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {e}") from e
        self.create_table()

    def __del__(self):
        try:
            self.finalize_statement()
        except Exception:
            pass
        try:
            if self.connection is not None:
                self.close_connection()
        except Exception:
            pass

    def prepare_statement(self, query):
        self.finalize_statement()
        self.query = query
        try:
            self.stmt = self.connection.cursor()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to prepare statement: {e}") from e

    def finalize_statement(self):
        if self.stmt is not None:
            self.stmt.close()
            self.stmt = None

    def insert_user(self, username, password):
        self.prepare_statement("INSERT INTO users (username, password) VALUES (?, ?)")
        try:
            self.stmt.execute(self.query, (username, password))
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {e}") from e
        self.finalize_statement()

    def search_user_by_username(self, username):
        self.prepare_statement("SELECT username, password FROM users WHERE username = ?")
        user = None
        row = self.stmt.execute(self.query, (username,)).fetchone()
        if row is not None:
            user = (row[0], row[1])
        self.finalize_statement()
        return user

    def delete_user_by_username(self, username):
        self.prepare_statement("DELETE FROM users WHERE username = ?")
        try:
            self.stmt.execute(self.query, (username,))
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {e}") from e
        self.finalize_statement()

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
            )
        """
        try:
            self.connection.execute(create_table_query)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {e}") from e

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None