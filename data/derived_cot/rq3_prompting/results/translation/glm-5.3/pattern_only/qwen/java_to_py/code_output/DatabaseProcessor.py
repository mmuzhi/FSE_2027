import sqlite3
import traceback
from contextlib import closing

# Note: the Java static block loads the SQLite JDBC driver; in Python,
# sqlite3 is built in, so no driver loading is needed.


class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        try:
            # isolation_level=None -> autocommit, matching JDBC default behavior
            with closing(sqlite3.connect(self.database_name, isolation_level=None)) as conn:
                create_table_query = (
                    "CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY, %s TEXT, %s INTEGER)"
                    % (table_name, key1, key2)
                )
                conn.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()

    def insert_into_database(self, table_name: str, data: list) -> None:
        try:
            with closing(sqlite3.connect(self.database_name, isolation_level=None)) as conn:
                for item in data:
                    # (int) item.get("age") in Java: null/non-int raises an
                    # uncaught exception (NPE/CCE); int(...) mirrors that here.
                    insert_query = "INSERT INTO %s (name, age) VALUES ('%s', %d)" % (
                        table_name,
                        item.get("name"),
                        int(item.get("age")),
                    )
                    conn.execute(insert_query)
        except sqlite3.Error:
            traceback.print_exc()

    def search_database(self, table_name: str, name: str):
        result = []
        try:
            with closing(sqlite3.connect(self.database_name, isolation_level=None)) as conn:
                select_query = "SELECT * FROM %s WHERE name = '%s'" % (table_name, name)
                cur = conn.execute(select_query)
                for row in cur.fetchall():
                    result.append({"id": row[0], "name": row[1], "age": row[2]})
        except sqlite3.Error:
            traceback.print_exc()
        return result if result else None

    def delete_from_database(self, table_name: str, name: str) -> None:
        try:
            with closing(sqlite3.connect(self.database_name, isolation_level=None)) as conn:
                delete_query = "DELETE FROM %s WHERE name = '%s'" % (table_name, name)
                conn.execute(delete_query)
        except sqlite3.Error:
            traceback.print_exc()