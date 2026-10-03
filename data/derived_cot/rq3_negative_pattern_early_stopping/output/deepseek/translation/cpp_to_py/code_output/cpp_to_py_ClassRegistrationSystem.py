from typing import List, Dict

class Student:
    def __init__(self, name: str, major: str):
        self.name = name
        self.major = major

    def get_name(self) -> str:
        return self.name

    def get_major(self) -> str:
        return self.major

    def set_name(self, name: str) -> None:
        self.name = name

    def set_major(self, major: str) -> None:
        self.major = major

    def __eq__(self, other: "Student") -> bool:
        return self.name == other.name and self.major == other.major


class ClassRegistrationSystem:
    def __init__(self):
        self.students: List[Student] = []
        self.students_registration_classes: Dict[str, List[str]] = {}

    def register_student(self, new_student: Student) -> int:
        name = new_student.get_name()
        major = new_student.get_major()
        for s in self.students:
            if s.get_name() == name:
                return 0
        self.students.append(Student(name, major))
        return 1

    def register_class(self, student_name: str, class_name: str) -> List[str]:
        if student_name not in self.students_registration_classes:
            self.students_registration_classes[student_name] = []
        classes = self.students_registration_classes[student_name]
        if class_name not in classes:
            classes.append(class_name)
        return classes

    def get_students_by_major(self, major: str) -> List[str]:
        result = []
        for s in self.students:
            if s.get_major() == major:
                result.append(s.get_name())
        return result

    def get_all_major(self) -> List[str]:
        majors = set()
        for s in self.students:
            majors.add(s.get_major())
        return sorted(majors)

    def get_most_popular_class_in_major(self, major: str) -> str:
        class_count = {}
        for s in self.students:
            if s.get_major() == major:
                classes = self.students_registration_classes.get(s.get_name())
                if classes is not None:
                    for c in classes:
                        class_count[c] = class_count.get(c, 0) + 1
        most_popular = ""
        max_count = 0
        for class_name, count in class_count.items():
            if count > max_count:
                most_popular = class_name
                max_count = count
        return most_popular