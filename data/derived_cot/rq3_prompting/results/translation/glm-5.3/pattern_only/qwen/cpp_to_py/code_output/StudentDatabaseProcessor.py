import sqlite3


class StudentDatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

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
        self.execute_query(create_table_query, [])

    def insert_student(self, student_data):
        insert_query = """
        INSERT INTO students (name, age, gender, grade)
        VALUES (?, ?, ?, ?)
    """
        params = [
            student_data["name"],
            student_data["age"],
            student_data["gender"],
            student_data["grade"],
        ]
        self.execute_query(insert_query, params)

    def search_student_by_name(self, name):
        select_query = """
        SELECT * FROM students WHERE name = ?
    """
        params = [name]
        results = self.query_result(select_query, params)

        students = []
        for row in results:
            student = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "grade": row[4],
            }
            students.append(student)
        return students

    def delete_student_by_name(self, name):
        delete_query = """
        DELETE FROM students WHERE name = ?
    """
        params = [name]
        self.execute_query(delete_query, params)

    def execute_query(self, query, params):
        try:
            conn = sqlite3.connect(self.database_name)
            try:
                conn.execute(query, params)
                # C++ code runs in autocommit mode; Python's sqlite3 opens an
                # implicit transaction for DML, so commit to persist changes.
                conn.commit()
            finally:
                conn.close()
        except sqlite3.Error:
            # C++ version ignores sqlite return codes (silent failure).
            pass

    def query_result(self, query, params):
        try:
            conn = sqlite3.connect(self.database_name)
            try:
                cursor = conn.execute(query, params)
                # sqlite3_column_text returns text representations of values.
                results = [[str(value) for value in row] for row in cursor.fetchall()]
            finally:
                conn.close()
            return results
        except sqlite3.Error:
            # On prepare/step failure the C++ loop simply ends; return what
            # amounts to no rows.
            return []