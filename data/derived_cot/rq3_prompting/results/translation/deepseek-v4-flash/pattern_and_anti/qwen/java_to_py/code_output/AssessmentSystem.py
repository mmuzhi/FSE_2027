class AssessmentSystem:
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
            total = sum(self.courses.values())
            return total / len(self.courses)

        def hasFailingCourse(self):
            return any(score < 60 for score in self.courses.values())

        def getCourseScore(self, course):
            return self.courses.get(course)

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(other) is not AssessmentSystem.Student:
                return False
            return (self.grade == other.grade and
                    self.name == other.name and
                    self.major == other.major and
                    self.courses == other.courses)

        def __hash__(self):
            return hash((self.name, self.grade, self.major, frozenset(self.courses.items())))

    def __init__(self):
        self.students = {}

    def addStudent(self, name, grade, major):
        self.students[name] = AssessmentSystem.Student(name, grade, major)

    def addCourseScore(self, name, course, score):
        if name in self.students:
            self.students[name].addCourseScore(course, score)

    def getGPA(self, name):
        if name in self.students:
            return self.students[name].calculateGPA()
        return None

    def getAllStudentsWithFailCourse(self):
        failing = []
        for student in self.students.values():
            if student.hasFailingCourse():
                failing.append(student.getName())
        return failing

    def getCourseAverage(self, course):
        total = 0
        count = 0
        for student in self.students.values():
            score = student.getCourseScore(course)
            if score is not None:
                total += score
                count += 1
        return total / count if count > 0 else None

    def getTopStudent(self):
        top_student = None
        top_gpa = 0
        for student in self.students.values():
            gpa = student.calculateGPA()
            if gpa is not None and gpa > top_gpa:
                top_gpa = gpa
                top_student = student.getName()
        return top_student


def java_to_string(obj):
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, list):
        return "[" + ", ".join(java_to_string(x) for x in obj) + "]"
    if isinstance(obj, dict):
        return "{" + ", ".join(java_to_string(k) + "=" + java_to_string(v) for k, v in obj.items()) + "}"
    return str(obj)


def java_print(obj):
    print(java_to_string(obj))


if __name__ == "__main__":
    system = AssessmentSystem()
    system.addStudent("student 1", 3, "SE")
    system.addStudent("student 2", 2, "SE")
    system.addCourseScore("student 1", "course 1", 86)
    system.addCourseScore("student 2", "course 1", 59)
    system.addCourseScore("student 1", "course 2", 78)
    system.addCourseScore("student 2", "course 2", 90)

    java_print(system.getAllStudentsWithFailCourse())
    java_print(system.getCourseAverage("course 1"))
    java_print(system.getCourseAverage("course 2"))
    java_print(system.getGPA("student 1"))
    java_print(system.getGPA("student 2"))
    java_print(system.getTopStudent())