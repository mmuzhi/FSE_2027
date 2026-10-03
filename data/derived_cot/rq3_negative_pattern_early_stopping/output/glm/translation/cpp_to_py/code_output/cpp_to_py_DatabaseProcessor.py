import sqlite3

class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def open_database(self):
        try:
            return sqlite3.connect(self.database_name)
        except sqlite3.Error as e:
            raise RuntimeError("Failed to open database") from e

    def create_table(self, table_name, key1, key2):
        db = self.open_database()
        cursor = db.cursor()
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        try:
            cursor.execute(create_table_query)
            db.commit()
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError(f"Failed to create table: {e}") from e
        db.close()

    def insert_into_database(self, table_name, data):
        db = self.open_database()
        cursor = db.cursor()
        insert_query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
        try:
            for item in data:
                name_val = item["name"]
                age_val = int(item["age"])
                cursor.execute(insert_query, (name_val, age_val))
            db.commit()
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError(f"Failed to execute statement: {e}") from e
        db.close()

    def search_database(self, table_name, name):
        result = []
        try:
            db = sqlite3.connect(self.database_name)
        except sqlite3.Error:
            return result
        
        cursor = db.cursor()
        query = f"SELECT * FROM {table_name} WHERE name = ?"
        try:
            cursor.execute(query, (name,))
            rows = cursor.fetchall()
            for row in rows:
                result_row = []
                for val in row:
                    if val is None:
                        result_row.append("")
                    else:
                        result_row.append(str(val))
                result.append(result_row)
        except sqlite3.Error:
            db.close()
            return result
        
        db.close()
        return result

    def delete_from_database(self, table_name, name):
        db = self.open_database()
        cursor = db.cursor()
        delete_query = f"DELETE FROM {table_name} WHERE name = ?"
        try:
            cursor.execute(delete_query, (name,))
            db.commit()
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError(f"Failed to execute statement: {e}") from e
        db.close()