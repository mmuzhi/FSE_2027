class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def get_name(self):
        return self.name

    def get_major(self):
        return self.major

    def set_name(self, name):
        self.name = name

    def set_major(self, major):
        self.major = major

    def __eq__(self, other):
        return self.name == other.name and self.major == other.major


class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, new_student):
        name = new_student.get_name()
        major = new_student.get_major()
        for student in self.students:
            if student.get_name() == name:
                return 0
        self.students.append(Student(name, major))
        return 1

    def register_class(self, student_name, class_name):
        classes = self.students_registration_classes.setdefault(student_name, [])
        if class_name not in classes:
            classes.append(class_name)
        return list(classes)

    def get_students_by_major(self, major):
        return [student.get_name() for student in self.students if student.get_major() == major]

    def get_all_major(self):
        return sorted({student.get_major() for student in self.students})

    def get_most_popular_class_in_major(self, major):
        class_count = {}
        for student in self.students:
            if student.get_major() == major:
                for class_name in self.students_registration_classes.get(student.get_name(), []):
                    class_count[class_name] = class_count.get(class_name, 0) + 1

        most_popular_class = ""
        max_count = 0
        for class_name, count in class_count.items():
            if count > max_count:
                most_popular_class = class_name
                max_count = count

        return most_popular_class