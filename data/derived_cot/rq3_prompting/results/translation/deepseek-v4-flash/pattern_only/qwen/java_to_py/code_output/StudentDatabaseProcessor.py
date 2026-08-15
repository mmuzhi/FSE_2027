import sqlite3
import traceback


class StudentDatabaseProcessor:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def _get_connection(self):
        db_name = self.databaseName if self.databaseName is not None else "null"
        return sqlite3.connect(db_name)

    def createStudentTable(self):
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
            stmt = conn.cursor()
            stmt.execute(create_table_query)
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def insertStudent(self, studentData):
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        conn = None
        try:
            conn = self._get_connection()
            pstmt = conn.cursor()
            pstmt.execute(
                insert_query,
                (studentData.getName(), studentData.getAge(), studentData.getGender(), studentData.getGrade()),
            )
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    def searchStudentByName(self, name):
        select_query = "SELECT * FROM students WHERE name = ?"
        result = []
        conn = None
        try:
            conn = self._get_connection()
            pstmt = conn.cursor()
            pstmt.execute(select_query, (name,))
            for row in pstmt:
                student = {
                    "id": row[0],
                    "name": row[1],
                    "age": row[2] if row[2] is not None else 0,
                    "gender": row[3],
                    "grade": row[4] if row[4] is not None else 0,
                }
                result.append(student)
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()
        return result

    def deleteStudentByName(self, name):
        delete_query = "DELETE FROM students WHERE name = ?"
        conn = None
        try:
            conn = self._get_connection()
            pstmt = conn.cursor()
            pstmt.execute(delete_query, (name,))
            conn.commit()
        except sqlite3.Error:
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()

    class StudentData:
        def __init__(self, name, age, gender, grade):
            self.name = name
            self.age = age
            self.gender = gender
            self.grade = grade

        def getName(self):
            return self.name

        def getAge(self):
            return self.age

        def getGender(self):
            return self.gender

        def getGrade(self):
            return self.grade