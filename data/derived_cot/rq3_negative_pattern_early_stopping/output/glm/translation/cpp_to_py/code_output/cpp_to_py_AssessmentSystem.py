from typing import Optional, Dict, List


class Student:
    def __init__(self, grade: int, major: str, courses: Dict[str, int] = None):
        self.grade = grade
        self.major = major
        self.courses = courses if courses is not None else {}


class AssessmentSystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, name: str, grade: int, major: str) -> None:
        self.students[name] = Student(grade, major, {})

    def add_course_score(self, name: str, course: str, score: int) -> None:
        if name in self.students:
            self.students[name].courses[course] = score

    def get_gpa(self, name: str) -> Optional[float]:
        if name in self.students:
            courses = self.students[name].courses
            if courses:
                return sum(courses.values()) / len(courses)
        return None

    def get_all_students_with_fail_course(self) -> List[str]:
        result = []
        for name, student in self.students.items():
            if any(score < 60 for score in student.courses.values()):
                result.append(name)
        return result

    def get_course_average(self, course: str) -> Optional[float]:
        total = 0
        count = 0
        for name, student in self.students.items():
            if course in student.courses:
                total += student.courses[course]
                count += 1
        if count > 0:
            return total / count
        return None

    def get_top_student(self) -> Optional[str]:
        top_student = None
        highest_gpa = None
        for name, student in self.students.items():
            gpa = self.get_gpa(name)
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student