class Student:
    def __init__(self, name, grade, major):
        self.name = name
        self.grade = grade
        self.major = major
        self.courses = {}

    def add_course_score(self, course, score):
        self.courses[course] = score

    def calculate_gpa(self):
        if not self.courses:
            return None
        total_score = sum(self.courses.values())
        return total_score / len(self.courses)

    def has_failing_course(self):
        for score in self.courses.values():
            if score < 60:
                return True
        return False

    def get_course_score(self, course):
        return self.courses.get(course)

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return (self.name == other.name and
                self.grade == other.grade and
                self.major == other.major and
                self.courses == other.courses)

    def __hash__(self):
        return hash((self.name, self.grade, self.major, tuple(sorted(self.courses.items()))))


class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = Student(name, grade, major)

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name].add_course_score(course, score)

    def get_gpa(self, name):
        if name in self.students:
            return self.students[name].calculate_gpa()
        return None

    def get_all_students_with_fail_course(self):
        failing_students = []
        for student in self.students.values():
            if student.has_failing_course():
                failing_students.append(student.name)
        return failing_students

    def get_course_average(self, course):
        total_score = 0
        count = 0
        for student in self.students.values():
            score = student.get_course_score(course)
            if score is not None:
                total_score += score
                count += 1
        return total_score / count if count > 0 else None

    def get_top_student(self):
        top_student = None
        top_gpa = 0
        for student in self.students.values():
            gpa = student.calculate_gpa()
            if gpa is not None and gpa > top_gpa:
                top_gpa = gpa
                top_student = student.name
        return top_student


if __name__ == '__main__':
    system = AssessmentSystem()
    system.add_student("student 1", 3, "SE")
    system.add_student("student 2", 2, "SE")
    system.add_course_score("student 1", "course 1", 86)
    system.add_course_score("student 2", "course 1", 59)
    system.add_course_score("student 1", "course 2", 78)
    system.add_course_score("student 2", "course 2", 90)

    print(system.get_all_students_with_fail_course())
    print(system.get_course_average("course 1"))
    print(system.get_course_average("course 2"))
    print(system.get_gpa("student 1"))
    print(system.get_gpa("student 2"))
    print(system.get_top_student())