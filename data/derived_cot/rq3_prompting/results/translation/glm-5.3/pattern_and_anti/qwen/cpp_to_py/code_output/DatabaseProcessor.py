import re
import sqlite3


class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def open_database(self):
        try:
            # isolation_level=None -> autocommit, matching raw sqlite3 C API behavior
            return sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    @staticmethod
    def _stoi(value):
        # Mimic std::stoi: parse leading integer (optional whitespace/sign), else throw
        m = re.match(r"\s*[+-]?\d+", value)
        if m is None:
            raise ValueError("stoi")
        return int(m.group(0))

    def create_table(self, table_name, key1, key2):
        db = self.open_database()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS " + table_name
            + " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)"
        )
        try:
            db.execute(create_table_query)
        except sqlite3.Error as err:
            raise RuntimeError("Failed to create table: " + str(err))
        finally:
            db.close()

    def insert_into_database(self, table_name, data):
        db = self.open_database()
        insert_query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)"
        cursor = db.cursor()
        try:
            # Emulate sqlite3_prepare_v2: compile/validate without executing
            cursor.execute("EXPLAIN " + insert_query)
            cursor.fetchall()
        except sqlite3.Error as err:
            db.close()
            raise RuntimeError("Failed to prepare statement: " + str(err))

        try:
            for item in data:
                name = item["name"]
                age = self._stoi(item["age"])
                try:
                    cursor.execute(insert_query, (name, age))
                except sqlite3.Error as err:
                    raise RuntimeError("Failed to execute statement: " + str(err))
        finally:
            db.close()

    def search_database(self, table_name, name):
        result = []
        try:
            db = sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            return result

        query = "SELECT * FROM " + table_name + " WHERE name = ?"
        try:
            cursor = db.execute(query, (name,))
        except sqlite3.Error:
            db.close()
            return result

        try:
            for row in cursor:
                # sqlite3_column_text semantics: NULL -> "", others -> text form
                result.append(["" if v is None else str(v) for v in row])
        except sqlite3.Error:
            pass
        db.close()
        return result

    def delete_from_database(self, table_name, name):
        db = self.open_database()
        delete_query = "DELETE FROM " + table_name + " WHERE name = ?"
        cursor = db.cursor()
        try:
            # Emulate sqlite3_prepare_v2: compile/validate without executing
            cursor.execute("EXPLAIN " + delete_query)
            cursor.fetchall()
        except sqlite3.Error as err:
            db.close()
            raise RuntimeError("Failed to prepare statement: " + str(err))

        try:
            try:
                cursor.execute(delete_query, (name,))
            except sqlite3.Error as err:
                raise RuntimeError("Failed to execute statement: " + str(err))
        finally:
            db.close()