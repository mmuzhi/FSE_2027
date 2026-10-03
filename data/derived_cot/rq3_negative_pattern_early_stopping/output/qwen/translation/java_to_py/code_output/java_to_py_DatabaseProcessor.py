import sqlite3
from typing import List, Dict, Optional

class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            if conn:
                conn.close()

    def insert_data(self, table_name: str, data: List[Dict[str, int]]) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            for item in data:
                name = item["name"]
                age = item["age"]
                query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
                cursor.execute(query, (name, age))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error during insertion: {e}")
        finally:
            if conn:
                conn.close()

    def search_data(self, table_name: str, name: str) -> Optional[List[Dict[str, int]]]:
        conn = None
        result = []
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name} WHERE name = ?"
            cursor.execute(query, (name,))
            for row in cursor.fetchall():
                record = {
                    "id": row[0],
                    "name": row[1],
                    "age": row[2]
                }
                result.append(record)
        except sqlite3.Error as e:
            print(f"SQLite error during search: {e}")
        finally:
            if conn:
                conn.close()
        return None if not result else result

    def delete_data(self, table_name: str, name: str) -> None:
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE name = ?"
            cursor.execute(query, (name,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error during deletion: {e}")
        finally:
            if conn:
                conn.close()