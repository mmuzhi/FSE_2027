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
        if not isinstance(other, Student):
            return False
        return self.name == other.name and self.major == other.major


class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}  # Maps student name to list of classes

    def register_student(self, new_student):
        name = new_student.get_name()
        major = new_student.get_major()
        for student in self.students:
            if student.get_name() == name:
                return 0
        self.students.append(Student(name, major))
        return 1

    def register_class(self, student_name, class_name):
        if student_name not in self.students_registration_classes:
            self.students_registration_classes[student_name] = []
        classes_list = self.students_registration_classes[student_name]
        if class_name not in classes_list:
            classes_list.append(class_name)
        return classes_list

    def get_students_by_major(self, major):
        student_list = []
        for student in self.students:
            if student.get_major() == major:
                student_list.append(student.get_name())
        return student_list

    def get_all_major(self):
        majors = set()
        for student in self.students:
            majors.add(student.get_major())
        return list(majors)

    def get_most_popular_class_in_major(self, major):
        from collections import defaultdict
        class_count = defaultdict(int)

        for student in self.students:
            if student.get_major() == major:
                student_name = student.get_name()
                if student_name in self.students_registration_classes:
                    for class_name in self.students_registration_classes[student_name]:
                        class_count[class_name] += 1

        if not class_count:
            return ""

        most_popular_class = max(class_count, key=class_count.get)
        return most_popular_class