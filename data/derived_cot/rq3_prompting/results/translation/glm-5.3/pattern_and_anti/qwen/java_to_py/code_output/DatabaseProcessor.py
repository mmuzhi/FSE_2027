import sqlite3
import traceback


class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            create_table_query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"(id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            )
            conn.execute(create_table_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def insert_into_database(self, table_name: str, data: list) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            for item in data:
                name = item.get("name")
                age = int(item.get("age"))  # raises TypeError on None, like Java's NPE
                insert_query = (
                    f"INSERT INTO {table_name} (name, age) "
                    f"VALUES ('{'null' if name is None else name}', {age})"
                )
                conn.execute(insert_query)
                conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def search_database(self, table_name: str, name: str):
        result = []
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            conn.row_factory = sqlite3.Row
            select_query = f"SELECT * FROM {table_name} WHERE name = '{name}'"
            cursor = conn.execute(select_query)
            for row in cursor:  # lazy iteration, like ResultSet.next()
                result.append({
                    "id": row["id"],
                    "name": row["name"],
                    "age": row["age"] if row["age"] is not None else 0,
                })
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()
        return result if result else None

    def delete_from_database(self, table_name: str, name: str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            delete_query = f"DELETE FROM {table_name} WHERE name = '{name}'"
            conn.execute(delete_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()