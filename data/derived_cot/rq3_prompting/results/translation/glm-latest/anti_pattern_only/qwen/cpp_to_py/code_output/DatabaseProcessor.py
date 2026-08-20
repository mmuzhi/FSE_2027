import re
import sqlite3


def _stoi(text):
    """Equivalent of std::stoi: parse a leading decimal integer, enforce 32-bit range.

    Raises ValueError for non-numeric input (std::invalid_argument) and
    OverflowError for out-of-range values (std::out_of_range).
    """
    match = re.match(r"[ \t\n\v\f\r]*([+-]?[0-9]+)", text)
    if match is None:
        raise ValueError("stoi")
    value = int(match.group(1))
    if value < -(2 ** 31) or value > 2 ** 31 - 1:
        raise OverflowError("stoi")
    return value


class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def _open_database(self):
        try:
            # isolation_level=None -> autocommit, matching sqlite3_open defaults
            return sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error as exc:
            raise RuntimeError("Failed to open database") from exc

    def create_table(self, table_name, key1, key2):
        db = self._open_database()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS " + table_name
            + " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)"
        )
        try:
            db.execute(create_table_query)
        except sqlite3.Error as err_msg:
            raise RuntimeError("Failed to create table: " + str(err_msg)) from err_msg
        finally:
            db.close()

    def insert_into_database(self, table_name, data):
        db = self._open_database()
        cursor = db.cursor()
        insert_query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)"
        try:
            # Compile the statement without executing any row (mirrors sqlite3_prepare_v2),
            # so prepare-time failures are reported even for empty data.
            try:
                cursor.execute("EXPLAIN " + insert_query, ("", 0))
            except sqlite3.Error as exc:
                raise RuntimeError("Failed to prepare statement: " + str(exc)) from exc
            for item in data:
                try:
                    cursor.execute(insert_query, (item["name"], _stoi(item["age"])))
                except sqlite3.Error as exc:
                    raise RuntimeError("Failed to execute statement: " + str(exc)) from exc
        finally:
            cursor.close()
            db.close()

    def search_database(self, table_name, name):
        result = []
        try:
            db = sqlite3.connect(self.database_name, isolation_level=None)
        except sqlite3.Error:
            return result

        query = "SELECT * FROM " + table_name + " WHERE name = ?"
        cursor = db.cursor()
        try:
            try:
                cursor.execute(query, (name,))
            except sqlite3.Error:
                return result

            while True:
                try:
                    row = cursor.fetchone()
                except sqlite3.Error:
                    break
                if row is None:
                    break
                result.append(["" if value is None else str(value) for value in row])
        finally:
            cursor.close()
            db.close()
        return result

    def delete_from_database(self, table_name, name):
        db = self._open_database()
        cursor = db.cursor()
        delete_query = "DELETE FROM " + table_name + " WHERE name = ?"
        try:
            # Compile-only pass so prepare failures are distinguished from step failures.
            try:
                cursor.execute("EXPLAIN " + delete_query, (name,))
            except sqlite3.Error as exc:
                raise RuntimeError("Failed to prepare statement: " + str(exc)) from exc
            try:
                cursor.execute(delete_query, (name,))
            except sqlite3.Error as exc:
                raise RuntimeError("Failed to execute statement: " + str(exc)) from exc
        finally:
            cursor.close()
            db.close()