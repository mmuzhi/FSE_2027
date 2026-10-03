import sqlite3
import traceback


class StudentDatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def createStudentTable(self) -> None:
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
            with self._get_connection() as conn:
                conn.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()

    def insertStudent(self, student_data: "StudentData") -> None:
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        try:
            with self._get_connection() as conn:
                conn.execute(
                    insert_query,
                    (
                        student_data.getName(),
                        student_data.getAge(),
                        student_data.getGender(),
                        student_data.getGrade(),
                    ),
                )
        except sqlite3.Error:
            traceback.print_exc()

    def searchStudentByName(self, name: str) -> list[dict[str, object]]:
        select_query = "SELECT * FROM students WHERE name = ?"
        result: list[dict[str, object]] = []
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(select_query, (name,))
                for row in cursor.fetchall():
                    student = {
                        "id": row[0],
                        "name": row[1],
                        "age": row[2],
                        "gender": row[3],
                        "grade": row[4],
                    }
                    result.append(student)
        except sqlite3.Error:
            traceback.print_exc()
        return result

    def deleteStudentByName(self, name: str) -> None:
        delete_query = "DELETE FROM students WHERE name = ?"
        try:
            with self._get_connection() as conn:
                conn.execute(delete_query, (name,))
        except sqlite3.Error:
            traceback.print_exc()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)


class StudentData:
    def __init__(self, name: str, age: int, gender: str, grade: int):
        self._name = name
        self._age = age
        self._gender = gender
        self._grade = grade

    def getName(self) -> str:
        return self._name

    def getAge(self) -> int:
        return self._age

    def getGender(self) -> str:
        return self._gender

    def getGrade(self) -> int:
        return self._grade