import sqlite3
import os
from typing import List, Dict

class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def _open_database(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_name)
        return conn

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        conn = self._open_database()
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            conn.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")
        finally:
            conn.close()

    def insert_into_database(self, table_name: str, data: List[Dict[str, str]]) -> None:
        conn = self._open_database()
        cur = conn.cursor()
        try:
            query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
            cur.execute(query, (None, None))  # dummy to check prepare? No, we need to bind per row.
            for item in data:
                cur.execute(query, (item["name"], int(item["age"])))
            conn.commit()
        except (sqlite3.Error, KeyError, ValueError) as e:
            raise RuntimeError(f"Failed to execute statement: {e}")
        finally:
            conn.close()

    def search_database(self, table_name: str, name: str) -> List[List[str]]:
        result: List[List[str]] = []
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            cur = conn.cursor()
            query = f"SELECT * FROM {table_name} WHERE name = ?"
            cur.execute(query, (name,))
            for row in cur.fetchall():
                result.append([str(col) if col is not None else "" for col in row])
        except sqlite3.Error:
            pass
        finally:
            if conn:
                conn.close()
        return result

    def delete_from_database(self, table_name: str, name: str) -> None:
        conn = self._open_database()
        cur = conn.cursor()
        try:
            query = f"DELETE FROM {table_name} WHERE name = ?"
            cur.execute(query, (name,))
            conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to execute statement: {e}")
        finally:
            conn.close()