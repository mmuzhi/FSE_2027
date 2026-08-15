import sqlite3
import traceback


class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def create_table(self, table_name, key1, key2):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            conn.isolation_level = None
            stmt = conn.cursor()
            create_table_query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"(id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            )
            stmt.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def insert_into_database(self, table_name, data):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            conn.isolation_level = None
            stmt = conn.cursor()
            for item in data:
                insert_query = (
                    f"INSERT INTO {table_name} (name, age) "
                    f"VALUES ('{item.get('name')}', {int(item.get('age'))})"
                )
                stmt.execute(insert_query)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def search_database(self, table_name, name):
        result = []
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            conn.isolation_level = None
            conn.row_factory = sqlite3.Row
            stmt = conn.cursor()
            select_query = f"SELECT * FROM {table_name} WHERE name = '{name}'"
            stmt.execute(select_query)
            for row in stmt.fetchall():
                result.append({
                    "id": row["id"],
                    "name": row["name"],
                    "age": row["age"],
                })
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()
        return result if result else None

    def delete_from_database(self, table_name, name):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            conn.isolation_level = None
            stmt = conn.cursor()
            delete_query = f"DELETE FROM {table_name} WHERE name = '{name}'"
            stmt.execute(delete_query)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()