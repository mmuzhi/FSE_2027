import sqlite3
from typing import Dict, List, Tuple, Optional

class StudentDatabaseProcessor:
    def __init__(self, database_name: str):
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
        self._execute_query(create_table_query, ())

    def insert_student(self, student_data: Dict[str, str]):
        # The C++ code expects a map with keys: "name", "age", "gender", "grade"
        # But note: the C++ code uses TEXT for age and grade, but in Python we can bind integers as well.
        # However, to match the C++ behavior (which uses TEXT for all), we convert everything to string?
        # But wait, the C++ code uses `sqlite3_bind_text` for all parameters. So we should bind all as TEXT.
        # However, the original C++ code expects the map to have string values. In Python, we can have mixed types.
        # Let's assume the input dictionary has string values for all fields, as in the C++ code.
        insert_query = """
            INSERT INTO students (name, age, gender, grade)
            VALUES (?, ?, ?, ?)
        """
        params = (
            student_data["name"],
            student_data["age"],
            student_data["gender"],
            student_data["grade"]
        )
        self._execute_query(insert_query, params)

    def search_student_by_name(self, name: str) -> List[Dict[str, str]]:
        select_query = """
            SELECT * FROM students WHERE name = ?
        """
        params = (name,)
        results = self._query_result(select_query, params)
        students = []
        for row in results:
            student = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "grade": row[4]
            }
            students.append(student)
        return students

    def delete_student_by_name(self, name: str):
        delete_query = """
            DELETE FROM students WHERE name = ?
        """
        params = (name,)
        self._execute_query(delete_query, params)

    def _execute_query(self, query: str, params: Tuple) -> None:
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def _query_result(self, query: str, params: Tuple) -> List[List[str]]:
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append(list(row))
        conn.close()
        return results

# Example usage (for testing):
if __name__ == "__main__":
    db = StudentDatabaseProcessor("students.db")
    db.create_student_table()
    db.insert_student({
        "name": "Alice",
        "age": "20",
        "gender": "F",
        "grade": "90"
    })
    db.insert_student({
        "name": "Bob",
        "age": "22",
        "gender": "M",
        "grade": "85"
    })
    students = db.search_student_by_name("Alice")
    for student in students:
        print(student)
    db.delete_student_by_name("Alice")