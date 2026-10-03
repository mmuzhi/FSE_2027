class ClassRegistrationSystem:
    class Student:
        def __init__(self, name: str, major: str):
            self.name = name
            self.major = major

        def get_name(self):
            return self.name

        def get_major(self):
            return self.major

        def __eq__(self, other):
            if not isinstance(other, self.__class__):
                return False
            return self.name == other.name and self.major == other.major

        def __hash__(self):
            return hash((self.name, self.major))

    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student: 'ClassRegistrationSystem.Student') -> int:
        if student in self.students:
            return 0
        else:
            self.students.append(student)
            return 1

    def register_class(self, student_name: str, class_name: str) -> list:
        if student_name in self.students_registration_classes:
            self.students_registration_classes[student_name].append(class_name)
        else:
            self.students_registration_classes[student_name] = [class_name]
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major: str) -> list:
        student_list = []
        for student in self.students:
            if student.get_major() == major:
                student_list.append(student.get_name())
        return student_list

    def get_all_major(self) -> list:
        major_set = set()
        for student in self.students:
            major_set.add(student.get_major())
        return list(major_set)

    def get_most_popular_class_in_major(self, major: str) -> str:
        class_count = {}
        for student in self.students:
            if student.get_major() == major:
                classes = self.students_registration_classes.get(student.get_name(), [])
                for class_name in classes:
                    class_count[class_name] = class_count.get(class_name, 0) + 1
        return max(class_count, key=class_count.get)

    def set_students(self, students: list):
        self.students = students

    def set_student_classes(self, student_classes: dict):
        self.students_registration_classes = student_classes