import sqlite3
from typing import Dict, List


class DatabaseProcessor:
    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def _open_database(self) -> sqlite3.Connection:
        try:
            # isolation_level=None -> autocommit, matching the C++ per-statement commit behavior
            return sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        db = self._open_database()
        try:
            create_table_query = (
                "CREATE TABLE IF NOT EXISTS " + table_name
                + " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)"
            )
            try:
                db.execute(create_table_query)
            except sqlite3.Error as e:
                raise RuntimeError("Failed to create table: " + str(e))
        finally:
            db.close()

    def insert_into_database(
        self, table_name: str, data: List[Dict[str, str]]
    ) -> None:
        db = self._open_database()
        try:
            insert_query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)"
            cursor = db.cursor()
            for item in data:
                # item["name"]/item["age"] raise KeyError like std::map::at;
                # int() raises ValueError like std::stoi on bad input
                try:
                    cursor.execute(insert_query, (item["name"], int(item["age"])))
                except sqlite3.Error as e:
                    raise RuntimeError("Failed to execute statement: " + str(e))
        finally:
            db.close()

    def search_database(self, table_name: str, name: str) -> List[List[str]]:
        result: List[List[str]] = []

        try:
            db = sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            return result

        try:
            query = "SELECT * FROM " + table_name + " WHERE name = ?"
            try:
                cursor = db.execute(query, (name,))
            except sqlite3.Error:
                return result

            while True:
                try:
                    row = cursor.fetchone()
                except sqlite3.Error:
                    break  # mid-iteration step failure: keep partial results, like the C++ loop
                if row is None:
                    break
                # sqlite3_column_text converts every column to text; NULL becomes ""
                result.append(["" if value is None else str(value) for value in row])
        finally:
            db.close()

        return result

    def delete_from_database(self, table_name: str, name: str) -> None:
        db = self._open_database()
        try:
            delete_query = "DELETE FROM " + table_name + " WHERE name = ?"
            try:
                db.execute(delete_query, (name,))
            except sqlite3.Error as e:
                raise RuntimeError("Failed to execute statement: " + str(e))
        finally:
            db.close()