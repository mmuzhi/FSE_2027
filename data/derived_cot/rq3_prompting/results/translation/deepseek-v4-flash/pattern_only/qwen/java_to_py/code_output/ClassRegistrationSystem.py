class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.studentsRegistrationClasses = {}

    def registerStudent(self, student):
        if student in self.students:
            return 0
        else:
            self.students.append(student)
            return 1

    def registerClass(self, studentName, className):
        if studentName in self.studentsRegistrationClasses:
            self.studentsRegistrationClasses[studentName].append(className)
        else:
            self.studentsRegistrationClasses[studentName] = [className]
        return self.studentsRegistrationClasses[studentName]

    def getStudentsByMajor(self, major):
        studentList = []
        for student in self.students:
            if student.getMajor() == major:
                studentList.append(student.getName())
        return studentList

    def getAllMajor(self):
        majorSet = set()
        for student in self.students:
            majorSet.add(student.getMajor())
        return list(majorSet)

    def getMostPopularClassInMajor(self, major):
        classCount = {}
        for student in self.students:
            if student.getMajor() == major:
                classes = self.studentsRegistrationClasses.get(student.getName(), [])
                for className in classes:
                    classCount[className] = classCount.get(className, 0) + 1
        return max(classCount.items(), key=lambda x: x[1])[0]

    def setStudents(self, students):
        self.students = students

    def setStudentClasses(self, studentClasses):
        self.studentsRegistrationClasses = studentClasses

    class Student:
        def __init__(self, name, major):
            self.name = name
            self.major = major

        def getName(self):
            return self.name

        def getMajor(self):
            return self.major

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return self.name == other.name and self.major == other.major

        def __hash__(self):
            return hash((self.name, self.major))