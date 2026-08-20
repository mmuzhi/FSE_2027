from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Student:
    grade: int
    major: str
    courses: Dict[str, int] = field(default_factory=dict)


class AssessmentSystem:
    def __init__(self) -> None:
        self.students: Dict[str, Student] = {}

    def add_student(self, name: str, grade: int, major: str) -> None:
        # Like std::map::operator[], re-adding a student replaces the entry
        # (resetting any previously recorded courses).
        self.students[name] = Student(grade, major)

    def add_course_score(self, name: str, course: str, score: int) -> None:
        student = self.students.get(name)
        if student is not None:
            student.courses[course] = score

    def get_gpa(self, name: str) -> Optional[float]:
        student = self.students.get(name)
        if student is not None:
            courses = student.courses
            if courses:  # non-empty, like !courses.empty()
                return sum(courses.values()) / len(courses)
        return None

    def get_all_students_with_fail_course(self) -> List[str]:
        # std::map iterates in sorted key order; mirror that ordering.
        students_with_fail: List[str] = []
        for name in sorted(self.students):
            if any(score < 60 for score in self.students[name].courses.values()):
                students_with_fail.append(name)
        return students_with_fail

    def get_course_average(self, course: str) -> Optional[float]:
        total = 0.0
        count = 0
        for name in sorted(self.students):
            courses = self.students[name].courses
            if course in courses:
                total += courses[course]
                count += 1
        return (total / count) if count > 0 else None

    def get_top_student(self) -> Optional[str]:
        top_student: Optional[str] = None
        highest_gpa: Optional[float] = None
        for name in sorted(self.students):
            gpa = self.get_gpa(name)
            # gpa having a value is what matters (even 0.0), hence "is not None".
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student