import sqlite3
from typing import List, Dict


class StudentDatabaseProcessor:
    """Manages a SQLite database of students."""

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def create_student_table(self) -> None:
        """Create the students table if it does not exist."""
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

    def insert_student(self, student_data: Dict[str, str]) -> None:
        """Insert a new student record.

        Args:
            student_data: Must contain keys 'name', 'age', 'gender', 'grade'.
        """
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
        self._execute_query(insert_query, params)

    def search_student_by_name(self, name: str) -> List[Dict[str, str]]:
        """Search for students with the given name.

        Returns:
            A list of dictionaries, each containing 'id', 'name', 'age',
            'gender', 'grade' as strings.
        """
        select_query = "SELECT * FROM students WHERE name = ?"
        params = [name]
        rows = self._query_result(select_query, params)

        students: List[Dict[str, str]] = []
        for row in rows:
            student = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "grade": row[4],
            }
            students.append(student)
        return students

    def delete_student_by_name(self, name: str) -> None:
        """Delete all students with the given name."""
        delete_query = "DELETE FROM students WHERE name = ?"
        params = [name]
        self._execute_query(delete_query, params)

    def _execute_query(self, query: str, params: List[str]) -> None:
        """Execute a query that does not return rows (INSERT, DELETE, CREATE, etc.).

        Autocommit is enabled to match the C++ default behavior.
        """
        conn = sqlite3.connect(self.database_name, isolation_level=None)
        conn.execute(query, params)
        conn.close()

    def _query_result(self, query: str, params: List[str]) -> List[List[str]]:
        """Execute a SELECT query and return all rows as lists of strings.

        Autocommit is enabled to match the C++ default behavior.
        """
        conn = sqlite3.connect(self.database_name, isolation_level=None)
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        result = [[str(col) for col in row] for row in rows]
        return result