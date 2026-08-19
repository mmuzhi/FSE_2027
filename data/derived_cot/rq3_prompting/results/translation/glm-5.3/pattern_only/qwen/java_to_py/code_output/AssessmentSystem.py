class Student:
    def __init__(self, name, grade, major):
        self.name = name
        self.grade = grade
        self.major = major
        self.courses = {}

    def getName(self):
        return self.name

    def addCourseScore(self, course, score):
        self.courses[course] = score

    def calculateGPA(self):
        if not self.courses:
            return None
        total_score = sum(self.courses.values())
        return total_score / len(self.courses)

    def hasFailingCourse(self):
        for score in self.courses.values():
            if score < 60:
                return True
        return False

    def getCourseScore(self, course):
        return self.courses.get(course)

    def __eq__(self, other):
        if self is other:
            return True
        if type(other) is not Student:
            return False
        return (self.grade == other.grade and
                self.name == other.name and
                self.major == other.major and
                self.courses == other.courses)

    def __hash__(self):
        return hash((self.name, self.grade, self.major, frozenset(self.courses.items())))


class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def addStudent(self, name, grade, major):
        self.students[name] = Student(name, grade, major)

    def addCourseScore(self, name, course, score):
        if name in self.students:
            self.students[name].addCourseScore(course, score)

    def getGPA(self, name):
        if name in self.students:
            return self.students[name].calculateGPA()
        return None

    def getAllStudentsWithFailCourse(self):
        failing_students = []
        for student in self.students.values():
            if student.hasFailingCourse():
                failing_students.append(student.getName())
        return failing_students

    def getCourseAverage(self, course):
        total_score = 0
        count = 0
        for student in self.students.values():
            score = student.getCourseScore(course)
            if score is not None:
                total_score += score
                count += 1
        return total_score / count if count > 0 else None

    def getTopStudent(self):
        top_student = None
        top_gpa = 0
        for student in self.students.values():
            gpa = student.calculateGPA()
            if gpa is not None and gpa > top_gpa:
                top_gpa = gpa
                top_student = student.getName()
        return top_student


if __name__ == "__main__":
    system = AssessmentSystem()
    system.addStudent("student 1", 3, "SE")
    system.addStudent("student 2", 2, "SE")
    system.addCourseScore("student 1", "course 1", 86)
    system.addCourseScore("student 2", "course 1", 59)
    system.addCourseScore("student 1", "course 2", 78)
    system.addCourseScore("student 2", "course 2", 90)

    print("[" + ", ".join(system.getAllStudentsWithFailCourse()) + "]")
    print(system.getCourseAverage("course 1"))
    print(system.getCourseAverage("course 2"))
    print(system.getGPA("student 1"))
    print(system.getGPA("student 2"))
    print(system.getTopStudent())