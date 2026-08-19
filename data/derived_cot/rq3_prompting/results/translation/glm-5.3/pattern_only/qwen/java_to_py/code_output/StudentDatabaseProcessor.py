import sqlite3
import traceback


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


def _as_int(value):
    # Mirrors JDBC ResultSet.getInt(): NULL becomes 0
    return 0 if value is None else int(value)


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
        conn = None
        try:
            conn = self._get_connection()
            conn.execute(create_table_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def insert_student(self, student_data):
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        conn = None
        try:
            conn = self._get_connection()
            conn.execute(
                insert_query,
                (student_data.name, student_data.age, student_data.gender, student_data.grade),
            )
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def search_student_by_name(self, name):
        select_query = "SELECT * FROM students WHERE name = ?"
        result = []
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(select_query, (name,))
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                student = {
                    "id": _as_int(record.get("id")),
                    "name": record.get("name"),
                    "age": _as_int(record.get("age")),
                    "gender": record.get("gender"),
                    "grade": _as_int(record.get("grade")),
                }
                result.append(student)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()
        return result

    def delete_student_by_name(self, name):
        delete_query = "DELETE FROM students WHERE name = ?"
        conn = None
        try:
            conn = self._get_connection()
            conn.execute(delete_query, (name,))
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.database_name)