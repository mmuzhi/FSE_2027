import sqlite3
from typing import List, Dict, Any

class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def _open_database(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to open database: {e}")

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        conn = self._open_database()
        cur = conn.cursor()
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        try:
            cur.execute(query)
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            raise RuntimeError(f"Failed to create table: {e}")
        conn.close()

    def insert_into_database(self, table_name: str, data: List[Dict[str, str]]) -> None:
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        params_list = []
        for item in data:
            if not isinstance(item, dict) or "name" not in item or "age" not in item:
                raise ValueError("Each item must be a dictionary containing 'name' and 'age'")
            try:
                name_val = item["name"]
                age_val = int(item["age"])
                params_list.append((name_val, age_val))
            except (ValueError, KeyError) as e:
                raise RuntimeError(f"Invalid data format: {str(e)}") from e

        query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
        conn = self._open_database()
        cur = conn.cursor()
        try:
            cur.executemany(query, params_list)
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            raise RuntimeError(f"Failed to insert data: {e}")
        conn.close()

    def search_database(self, table_name: str, name: str) -> List[List[str]]:
        query = f"SELECT * FROM {table_name} WHERE name = ?"
        conn = self._open_database()
        cur = conn.cursor()
        try:
            cur.execute(query, (name,))
            result = []
            for row in cur.fetchall():
                row_data = []
                for col_value in row:
                    row_data.append(str(col_value) if col_value is not None else '')
                result.append(row_data)
            return result
        except sqlite3.Error as e:
            conn.close()
            raise RuntimeError(f"Failed to search database: {e}")
        finally:
            conn.close()

    def delete_from_database(self, table_name: str, name: str) -> None:
        query = f"DELETE FROM {table_name} WHERE name = ?"
        conn = self._open_database()
        cur = conn.cursor()
        try:
            cur.execute(query, (name,))
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            raise RuntimeError(f"Failed to delete data: {e}")
        conn.close()