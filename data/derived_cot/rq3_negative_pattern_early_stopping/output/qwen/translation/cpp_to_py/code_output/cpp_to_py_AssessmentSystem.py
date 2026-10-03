class Student:
    def __init__(self, grade, major):
        self.grade = grade
        self.major = major
        self.courses = {}  # map from course name to score

class AssessmentSystem:
    def __init__(self):
        self.students = {}  # map from name to Student

    def add_student(self, name, grade, major):
        self.students[name] = Student(grade, major)

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name].courses[course] = score

    def get_gpa(self, name):
        if name not in self.students:
            return None
        student = self.students[name]
        if not student.courses:
            return None
        total_score = sum(score for score in student.courses.values())
        return total_score / len(student.courses)

    def get_all_students_with_fail_course(self):
        students_with_fail = []
        for name, student in self.students.items():
            # Check if any course score is below 60
            if any(score < 60 for score in student.courses.values()):
                students_with_fail.append(name)
        return students_with_fail

    def get_course_average(self, course):
        total = 0
        count = 0
        for student in self.students.values():
            if course in student.courses:
                total += student.courses[course]
                count += 1
        if count == 0:
            return None
        return total / count

    def get_top_student(self):
        if not self.students:
            return None
        top_name = None
        highest_gpa = -1
        for name, student in self.students.items():
            gpa = self.get_gpa(name)
            if gpa is None:
                continue
            if top_name is None or gpa > highest_gpa:
                highest_gpa = gpa
                top_name = name
        return top_name