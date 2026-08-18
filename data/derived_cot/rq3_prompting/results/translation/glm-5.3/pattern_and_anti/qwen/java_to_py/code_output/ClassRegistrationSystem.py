from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Student:
    name: str
    major: str


class ClassRegistrationSystem:
    def __init__(self):
        self.students: List[Student] = []
        self.students_registration_classes: Dict[str, List[str]] = {}

    def register_student(self, student: Student) -> int:
        if student in self.students:
            return 0
        else:
            self.students.append(student)
            return 1

    def register_class(self, student_name: str, class_name: str) -> List[str]:
        if student_name in self.students_registration_classes:
            self.students_registration_classes[student_name].append(class_name)
        else:
            self.students_registration_classes[student_name] = [class_name]
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major: str) -> List[str]:
        return [student.name for student in self.students if student.major == major]

    def get_all_major(self) -> List[str]:
        return list({student.major for student in self.students})

    def get_most_popular_class_in_major(self, major: str) -> str:
        class_count: Dict[str, int] = {}
        for student in self.students:
            if student.major == major:
                classes = self.students_registration_classes.get(student.name, [])
                for class_name in classes:
                    class_count[class_name] = class_count.get(class_name, 0) + 1
        return max(class_count, key=class_count.get)

    # Setter methods for tests
    def set_students(self, students: List[Student]) -> None:
        self.students = students

    def set_student_classes(self, student_classes: Dict[str, List[str]]) -> None:
        self.students_registration_classes = student_classes