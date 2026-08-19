from dataclasses import dataclass, field


@dataclass
class Student:
    grade: int
    major: str
    courses: dict = field(default_factory=dict)


class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = Student(grade, major, {})

    def add_course_score(self, name, course, score):
        student = self.students.get(name)
        if student is not None:
            student.courses[course] = score

    def get_gpa(self, name):
        student = self.students.get(name)
        if student is not None and student.courses:
            return sum(student.courses.values()) / len(student.courses)
        return None

    def get_all_students_with_fail_course(self):
        return [
            name for name in sorted(self.students)
            if any(score < 60 for score in self.students[name].courses.values())
        ]

    def get_course_average(self, course):
        total = 0
        count = 0
        for name in sorted(self.students):
            courses = self.students[name].courses
            if course in courses:
                total += courses[course]
                count += 1
        return total / count if count > 0 else None

    def get_top_student(self):
        top_student = None
        highest_gpa = None
        for name in sorted(self.students):
            gpa = self.get_gpa(name)
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student