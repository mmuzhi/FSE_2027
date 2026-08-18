from typing import Optional, Dict, List


class Student:
    def __init__(self, grade: int, major: str, courses: Optional[Dict[str, int]] = None):
        self.grade: int = grade
        self.major: str = major
        self.courses: Dict[str, int] = courses if courses is not None else {}


class AssessmentSystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, name: str, grade: int, major: str) -> None:
        # Overwrites any existing entry with a fresh course list (same as C++ assignment)
        self.students[name] = Student(grade, major, {})

    def add_course_score(self, name: str, course: str, score: int) -> None:
        student = self.students.get(name)
        if student is not None:
            student.courses[course] = score

    def get_gpa(self, name: str) -> Optional[float]:
        student = self.students.get(name)
        if student is not None:
            courses = student.courses
            if courses:
                total_score = float(sum(courses.values()))
                return total_score / len(courses)
        return None

    def get_all_students_with_fail_course(self) -> List[str]:
        students_with_fail = []
        # std::map iterates in sorted key order; replicate that ordering
        for name in sorted(self.students.keys()):
            student = self.students[name]
            if any(score < 60 for score in student.courses.values()):
                students_with_fail.append(name)
        return students_with_fail

    def get_course_average(self, course: str) -> Optional[float]:
        total = 0
        count = 0
        for name in sorted(self.students.keys()):
            student = self.students[name]
            if course in student.courses:
                total += student.courses[course]
                count += 1
        return (total / count) if count > 0 else None

    def get_top_student(self) -> Optional[str]:
        top_student: Optional[str] = None
        highest_gpa: Optional[float] = None
        for name in sorted(self.students.keys()):
            gpa = self.get_gpa(name)
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student