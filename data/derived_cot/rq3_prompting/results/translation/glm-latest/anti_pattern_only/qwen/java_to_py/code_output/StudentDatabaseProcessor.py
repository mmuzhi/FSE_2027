import sqlite3
import traceback
from contextlib import closing
from typing import Any, Dict, List


class StudentDatabaseProcessor:
    class StudentData:
        """Student record (Java: public static class StudentData)."""

        def __init__(self, name: str, age: int, gender: str, grade: int) -> None:
            self.name = name
            self.age = age
            self.gender = gender
            self.grade = grade

        def get_name(self) -> str:
            return self.name

        def get_age(self) -> int:
            return self.age

        def get_gender(self) -> str:
            return self.gender

        def get_grade(self) -> int:
            return self.grade

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def create_student_table(self) -> None:
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
            with closing(self._get_connection()) as conn, closing(conn.cursor()) as stmt:
                stmt.execute(create_table_query)
        except sqlite3.Error:
            traceback.print_exc()

    def insert_student(self, student_data: StudentData) -> None:
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        try:
            with closing(self._get_connection()) as conn, closing(conn.cursor()) as pstmt:
                pstmt.execute(
                    insert_query,
                    (
                        student_data.get_name(),
                        student_data.get_age(),
                        student_data.get_gender(),
                        student_data.get_grade(),
                    ),
                )
        except sqlite3.Error:
            traceback.print_exc()

    def search_student_by_name(self, name: str) -> List[Dict[str, Any]]:
        select_query = "SELECT * FROM students WHERE name = ?"
        result: List[Dict[str, Any]] = []
        try:
            with closing(self._get_connection()) as conn, closing(conn.cursor()) as pstmt:
                pstmt.row_factory = sqlite3.Row
                pstmt.execute(select_query, (name,))  # 设置查询参数
                # 游标同时充当 ResultSet；逐行迭代相当于 while (rs.next())
                for row in pstmt:
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

    def delete_student_by_name(self, name: str) -> None:
        delete_query = "DELETE FROM students WHERE name = ?"
        try:
            with closing(self._get_connection()) as conn, closing(conn.cursor()) as pstmt:
                pstmt.execute(delete_query, (name,))
        except sqlite3.Error:
            traceback.print_exc()

    def _get_connection(self) -> sqlite3.Connection:
        # JDBC connections run in autocommit mode by default;
        # isolation_level=None reproduces that behavior with sqlite3.
        return sqlite3.connect(self.database_name, isolation_level=None)

    @staticmethod
    def _get_int(value: Any) -> Any:
        # Mimics JDBC ResultSet.getInt(), which returns 0 for SQL NULL.
        return 0 if value is None else value


# In Java, StudentData is a nested public static class of StudentDatabaseProcessor;
# this alias makes it equally usable at module level.
StudentData = StudentDatabaseProcessor.StudentData