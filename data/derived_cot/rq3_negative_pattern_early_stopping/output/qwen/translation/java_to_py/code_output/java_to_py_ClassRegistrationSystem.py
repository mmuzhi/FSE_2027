class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.name == other.name and self.major == other.major
        return False

    def __hash__(self):
        return hash((self.name, self.major))


class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        if any(s.name == student.name and s.major == student.major for s in self.students):
            return 0
        self.students.append(student)
        return 1

    def register_class(self, student_name, class_name):
        if student_name not in self.students_registration_classes:
            self.students_registration_classes[student_name] = []
        self.students_registration_classes[student_name].append(class_name)
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major):
        return [s.name for s in self.students if s.major == major]

    def get_all_major(self):
        return list({s.major for s in self.students})

    def get_most_popular_class_in_major(self, major):
        class_count = {}
        for student in self.students:
            if student.major == major:
                if student.name in self.students_registration_classes:
                    for cls in self.students_registration_classes[student.name]:
                        class_count[cls] = class_count.get(cls, 0) + 1
        if not class_count:
            return ""
        most_popular = max(class_count.items(), key=lambda x: x[1])
        return most_popular[0]