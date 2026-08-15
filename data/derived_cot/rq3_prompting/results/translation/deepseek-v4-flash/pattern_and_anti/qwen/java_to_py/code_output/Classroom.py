from datetime import time


class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def addCourse(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def removeCourse(self, course):
        try:
            self.courses.remove(course)
        except ValueError:
            pass

    def isFreeAt(self, checkTime):
        t = time.fromisoformat(checkTime)
        for course in self.courses:
            if course.startTime <= t <= course.endTime:
                return False
        return True

    def checkCourseConflict(self, newCourse):
        new_start = newCourse.startTime
        new_end = newCourse.endTime
        for course in self.courses:
            if new_end >= course.startTime and new_start <= course.endTime:
                return False
        return True