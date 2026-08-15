class NullPointerException(Exception):
    pass

class NoSuchElementException(Exception):
    pass

class ClassRegistrationSystem:
    class Student:
        def __init__(self, name, major):
            self._name = name
            self._major = major

        def getName(self):
            return self._name

        def getMajor(self):
            return self._major

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return self._name == other._name and self._major == other._major

        def __hash__(self):
            return hash((self._name, self._major))

    def __init__(self):
        self._students = []
        self._studentsRegistrationClasses = {}

    def _get_student_major(self, student):
        if student is None:
            raise NullPointerException()
        return student.getMajor()

    def _student_major_equals(self, student, major):
        major_value = self._get_student_major(student)
        if major_value is None:
            raise NullPointerException()
        return major_value == major

    def registerStudent(self, student):
        if student in self._students:
            return 0
        else:
            self._students.append(student)
            return 1

    def registerClass(self, studentName, className):
        if studentName in self._studentsRegistrationClasses:
            self._studentsRegistrationClasses[studentName].append(className)
        else:
            self._studentsRegistrationClasses[studentName] = [className]
        return self._studentsRegistrationClasses[studentName]

    def getStudentsByMajor(self, major):
        studentList = []
        for student in self._students:
            if self._student_major_equals(student, major):
                studentList.append(student.getName())
        return studentList

    def getAllMajor(self):
        majorSet = {}
        for student in self._students:
            major = self._get_student_major(student)
            majorSet[major] = None
        return list(majorSet.keys())

    def getMostPopularClassInMajor(self, major):
        classCount = {}
        for student in self._students:
            if self._student_major_equals(student, major):
                classes = self._studentsRegistrationClasses.get(student.getName(), [])
                for className in classes:
                    classCount[className] = classCount.get(className, 0) + 1
        if not classCount:
            raise NoSuchElementException()
        return max(classCount, key=classCount.get)

    def setStudents(self, students):
        self._students = students

    def setStudentClasses(self, studentClasses):
        self._studentsRegistrationClasses = studentClasses