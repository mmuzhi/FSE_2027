from datetime import time

from classroom_management_test import Course


class Classroom:
    def __init__(self, id: int):
        self.id = id
        self.courses = []

    def addCourse(self, course: Course) -> None:
        # Java's List.contains uses equals(); Python's `in` uses __eq__.
        if course not in self.courses:
            self.courses.append(course)

    def removeCourse(self, course: Course) -> None:
        # Java's List.remove(Object) removes the first equal element and is a
        # no-op (returns false) when absent; list.remove raises ValueError instead.
        try:
            self.courses.remove(course)
        except ValueError:
            pass

    def isFreeAt(self, checkTime: str) -> bool:
        t = time.fromisoformat(checkTime)
        for course in self.courses:
            if not t < course.startTime and not t > course.endTime:
                return False
        return True

    def checkCourseConflict(self, newCourse: Course) -> bool:
        newStartTime = newCourse.startTime
        newEndTime = newCourse.endTime

        for course in self.courses:
            if not (newEndTime < course.startTime or newStartTime > course.endTime):
                return False
        return True