import sqlite3
import traceback

class DatabaseProcessor:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def createTable(self, tableName, key1, key2):
        try:
            conn = sqlite3.connect(self.databaseName)
            cur = conn.cursor()
            create_query = f"CREATE TABLE IF NOT EXISTS {tableName} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            cur.execute(create_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            try:
                cur.close()
                conn.close()
            except Exception:
                pass

    def insertIntoDatabase(self, tableName, data):
        try:
            conn = sqlite3.connect(self.databaseName)
            cur = conn.cursor()
            for item in data:
                insert_query = f"INSERT INTO {tableName} (name, age) VALUES ('{item['name']}', {int(item['age'])})"
                cur.execute(insert_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            try:
                cur.close()
                conn.close()
            except Exception:
                pass

    def searchDatabase(self, tableName, name):
        result = []
        try:
            conn = sqlite3.connect(self.databaseName)
            cur = conn.cursor()
            select_query = f"SELECT * FROM {tableName} WHERE name = '{name}'"
            cur.execute(select_query)
            rows = cur.fetchall()
            for row in rows:
                result.append({'id': row[0], 'name': row[1], 'age': row[2]})
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            try:
                cur.close()
                conn.close()
            except Exception:
                pass
        return None if not result else result

    def deleteFromDatabase(self, tableName, name):
        try:
            conn = sqlite3.connect(self.databaseName)
            cur = conn.cursor()
            delete_query = f"DELETE FROM {tableName} WHERE name = '{name}'"
            cur.execute(delete_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            try:
                cur.close()
                conn.close()
            except Exception:
                pass