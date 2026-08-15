class Student:
    def __init__(self, grade, major):
        self.grade = grade
        self.major = major
        self.courses = {}


class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = Student(grade, major)

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name].courses[course] = score

    def get_gpa(self, name):
        student = self.students.get(name)
        if student is None or not student.courses:
            return None
        total = 0.0
        for course in sorted(student.courses):
            total += student.courses[course]
        return total / len(student.courses)

    def get_all_students_with_fail_course(self):
        result = []
        for name in sorted(self.students):
            student = self.students[name]
            if any(student.courses[course] < 60 for course in sorted(student.courses)):
                result.append(name)
        return result

    def get_course_average(self, course):
        total = 0.0
        count = 0
        for name in sorted(self.students):
            student = self.students[name]
            if course in student.courses:
                total += student.courses[course]
                count += 1
        if count > 0:
            return total / count
        return None

    def get_top_student(self):
        top_student = None
        highest_gpa = None
        for name in sorted(self.students):
            gpa = self.get_gpa(name)
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student