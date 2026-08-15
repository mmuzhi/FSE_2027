class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = {'grade': grade, 'major': major, 'courses': {}}

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name]['courses'][course] = score

    def get_gpa(self, name):
        if name in self.students:
            courses = self.students[name]['courses']
            if courses:
                return sum(courses.values()) / len(courses)
        return None

    def get_all_students_with_fail_course(self):
        result = []
        for name in sorted(self.students.keys()):
            student = self.students[name]
            if any(score < 60 for score in student['courses'].values()):
                result.append(name)
        return result

    def get_course_average(self, course):
        total = 0
        count = 0
        for name in sorted(self.students.keys()):
            student = self.students[name]
            if course in student['courses']:
                total += student['courses'][course]
                count += 1
        if count > 0:
            return total / count
        return None

    def get_top_student(self):
        top_student = None
        highest_gpa = None
        for name in sorted(self.students.keys()):
            gpa = self.get_gpa(name)
            if gpa is not None and (highest_gpa is None or gpa > highest_gpa):
                highest_gpa = gpa
                top_student = name
        return top_student