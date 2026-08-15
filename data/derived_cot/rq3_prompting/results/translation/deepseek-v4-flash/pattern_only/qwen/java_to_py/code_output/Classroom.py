import datetime


class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def addCourse(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def removeCourse(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def isFreeAt(self, checkTime):
        time = self._parse_time(checkTime)
        for course in self.courses:
            if not time < course.startTime and not time > course.endTime:
                return False
        return True

    def checkCourseConflict(self, newCourse):
        newStartTime = newCourse.startTime
        newEndTime = newCourse.endTime

        for course in self.courses:
            if not (newEndTime < course.startTime or newStartTime > course.endTime):
                return False
        return True

    @staticmethod
    def _parse_time(s):
        try:
            t = datetime.time.fromisoformat(s)
        except ValueError:
            t = datetime.time.fromisoformat(s + ":00")
        if t.tzinfo is not None:
            raise ValueError(f"Invalid time: {s}")
        return t