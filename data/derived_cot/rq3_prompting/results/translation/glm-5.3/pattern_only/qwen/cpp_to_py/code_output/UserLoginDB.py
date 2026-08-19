import sqlite3


class UserLoginDB:
    def __init__(self, db_name):
        self._connection = None
        self._stmt = None
        try:
            # isolation_level=None -> autocommit, mirroring sqlite3_step()'s
            # default autocommit behavior in the C code (no pending transaction).
            self._connection = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot open database: {e}") from None
        self.create_table()

    def __del__(self):
        # Mirrors the C++ destructor: finalize statement, then close connection.
        try:
            self._finalize_statement()
            self.close_connection()
        except Exception:
            pass

    def _prepare_statement(self, query):
        self._finalize_statement()
        self._stmt = self._connection.cursor()

    def _finalize_statement(self):
        if self._stmt is not None:
            self._stmt.close()
            self._stmt = None

    def insert_user(self, username, password):
        self._prepare_statement("INSERT INTO users (username, password) VALUES (?, ?)")
        try:
            self._stmt.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert user: {e}") from None
        finally:
            self._finalize_statement()

    def search_user_by_username(self, username):
        self._prepare_statement("SELECT username, password FROM users WHERE username = ?")
        try:
            self._stmt.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (username,),
            )
            row = self._stmt.fetchone()
        finally:
            self._finalize_statement()
        if row is not None:
            return (row[0], row[1])
        return None

    def delete_user_by_username(self, username):
        self._prepare_statement("DELETE FROM users WHERE username = ?")
        try:
            self._stmt.execute(
                "DELETE FROM users WHERE username = ?",
                (username,),
            )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete user: {e}") from None
        finally:
            self._finalize_statement()

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
            self._connection.execute(create_table_query)
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot create table: {e}") from None

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None