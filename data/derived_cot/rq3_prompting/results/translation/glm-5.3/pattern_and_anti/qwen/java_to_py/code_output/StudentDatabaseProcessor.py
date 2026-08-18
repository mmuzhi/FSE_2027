import sqlite3
import traceback
from contextlib import closing


class StudentData:
    def __init__(self, name, age, gender, grade):
        self.name = name
        self.age = age
        self.gender = gender
        self.grade = grade

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_gender(self):
        return self.gender

    def get_grade(self):
        return self.grade


class StudentDatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def create_student_table(self):
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER"
            ")"
        )
        try:
            with closing(self._get_connection()) as conn, conn:
                conn.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()

    def insert_student(self, student_data):
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        try:
            with closing(self._get_connection()) as conn, conn:
                conn.execute(
                    insert_query,
                    (
                        student_data.name,
                        student_data.age,
                        student_data.gender,
                        student_data.grade,
                    ),
                )
        except sqlite3.Error:
            traceback.print_exc()

    def search_student_by_name(self, name):
        select_query = "SELECT * FROM students WHERE name = ?"
        result = []
        try:
            with closing(self._get_connection()) as conn, conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(select_query, (name,))
                for row in cursor.fetchall():
                    student = {
                        "id": self._get_int(row["id"]),
                        "name": row["name"],
                        "age": self._get_int(row["age"]),
                        "gender": row["gender"],
                        "grade": self._get_int(row["grade"]),
                    }
                    result.append(student)
        except sqlite3.Error:
            traceback.print_exc()
        return result

    def delete_student_by_name(self, name):
        delete_query = "DELETE FROM students WHERE name = ?"
        try:
            with closing(self._get_connection()) as conn, conn:
                conn.execute(delete_query, (name,))
        except sqlite3.Error:
            traceback.print_exc()

    def _get_connection(self):
        return sqlite3.connect(self.database_name)

    @staticmethod
    def _get_int(value):
        # Mimics JDBC ResultSet.getInt(): NULL becomes 0
        return 0 if value is None else value