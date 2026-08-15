import sqlite3


class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def _open_database(self):
        try:
            return sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def create_table(self, table_name, key1, key2):
        db = self._open_database()
        query = (
            "CREATE TABLE IF NOT EXISTS " + table_name +
            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)"
        )
        try:
            db.execute(query)
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError("Failed to create table: " + str(e))
        db.close()

    def insert_into_database(self, table_name, data):
        db = self._open_database()
        query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)"
        cursor = db.cursor()
        try:
            for item in data:
                name = item["name"]
                age = int(item["age"])
                cursor.execute(query, (name, age))
        except sqlite3.Error as e:
            msg = str(e)
            if "syntax error" in msg or "incomplete input" in msg or "unrecognized token" in msg:
                prefix = "Failed to prepare statement"
            else:
                prefix = "Failed to execute statement"
            db.close()
            raise RuntimeError(prefix + ": " + msg)
        db.close()

    def search_database(self, table_name, name):
        try:
            db = sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            return []

        try:
            cursor = db.cursor()
            query = "SELECT * FROM " + table_name + " WHERE name = ?"
            cursor.execute(query, (name,))
            rows = cursor.fetchall()
        except sqlite3.Error:
            db.close()
            return []

        result = []
        for row in rows:
            converted_row = []
            for value in row:
                if value is None:
                    converted_row.append("")
                elif isinstance(value, bytes):
                    converted_row.append(value.decode("utf-8", "replace"))
                else:
                    converted_row.append(str(value))
            result.append(converted_row)

        db.close()
        return result

    def delete_from_database(self, table_name, name):
        db = self._open_database()
        query = "DELETE FROM " + table_name + " WHERE name = ?"
        cursor = db.cursor()
        try:
            cursor.execute(query, (name,))
        except sqlite3.Error as e:
            msg = str(e)
            if "syntax error" in msg or "incomplete input" in msg or "unrecognized token" in msg:
                prefix = "Failed to prepare statement"
            else:
                prefix = "Failed to execute statement"
            db.close()
            raise RuntimeError(prefix + ": " + msg)
        db.close()