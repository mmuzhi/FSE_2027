import sqlite3
from typing import List, Dict, Optional

class StudentDatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_student_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            grade INTEGER
        )
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
        except sqlite3.Error as error:
            print(f"Failed to create table: {error}")
        finally:
            if 'connection' in locals():
                connection.close()

    def insert_student(self, student_data):
        insert_query = """
        INSERT INTO students (name, age, gender, grade)
        VALUES (?, ?, ?, ?)
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(insert_query, (
                student_data.name,
                student_data.age,
                student_data.gender,
                student_data.grade
            ))
            connection.commit()
        except sqlite3.Error as error:
            print(f"Failed to insert student: {error}")
        finally:
            if 'connection' in locals():
                connection.close()

    def search_student_by_name(self, name: str) -> List[Dict[str, int]]:
        select_query = "SELECT * FROM students WHERE name = ?"
        result: List[Dict[str, int]] = []
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(select_query, (name,))
            for row in cursor.fetchall():
                student = {
                    "id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "gender": row[3],
                    "grade": row[4]
                }
                result.append(student)
        except sqlite3.Error as error:
            print(f"Failed to search student: {error}")
        finally:
            if 'connection' in locals():
                connection.close()
        return result

    def delete_student_by_name(self, name: str):
        delete_query = "DELETE FROM students WHERE name = ?"
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(delete_query, (name,))
            connection.commit()
        except sqlite3.Error as error:
            print(f"Failed to delete student: {error}")
        finally:
            if 'connection' in locals():
                connection.close()

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)

    class StudentData:
        __slots__ = ('name', 'age', 'gender', 'grade')
        def __init__(self, name: str, age: int, gender: str, grade: int):
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