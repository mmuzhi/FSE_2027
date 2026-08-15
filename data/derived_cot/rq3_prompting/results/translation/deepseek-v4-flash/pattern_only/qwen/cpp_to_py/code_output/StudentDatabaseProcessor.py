import sqlite3

class StudentDatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name.split('\0', 1)[0]

    def create_student_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                grade INTEGER
            )
        """
        self._execute_query(create_table_query, [])

    def insert_student(self, student_data):
        insert_query = """
            INSERT INTO students (name, age, gender, grade)
            VALUES (?, ?, ?, ?)
        """
        params = [
            student_data["name"],
            student_data["age"],
            student_data["gender"],
            student_data["grade"]
        ]
        self._execute_query(insert_query, params)

    def search_student_by_name(self, name):
        select_query = """
            SELECT * FROM students WHERE name = ?
        """
        params = [name]
        results = self._query_result(select_query, params)

        students = []
        for row in results:
            student = {
                "age": row[2],
                "gender": row[3],
                "grade": row[4],
                "id": row[0],
                "name": row[1],
            }
            students.append(student)
        return students

    def delete_student_by_name(self, name):
        delete_query = """
            DELETE FROM students WHERE name = ?
        """
        params = [name]
        self._execute_query(delete_query, params)

    def _execute_query(self, query, params):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name, timeout=0)
            conn.execute(query, [p.split('\0', 1)[0] for p in params])
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            if conn is not None:
                conn.close()

    def _query_result(self, query, params):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name, timeout=0)
            cursor = conn.execute(query, [p.split('\0', 1)[0] for p in params])
            results = []
            while True:
                try:
                    row = cursor.fetchone()
                except sqlite3.Error:
                    break
                if row is None:
                    break
                results.append([str(value) for value in row])
            return results
        except sqlite3.Error:
            return []
        finally:
            if conn is not None:
                conn.close()