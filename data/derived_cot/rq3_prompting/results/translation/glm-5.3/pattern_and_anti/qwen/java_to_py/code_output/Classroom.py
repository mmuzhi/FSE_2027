from datetime import time
from typing import Any, List


class Classroom:
    # Courses are duck-typed (expected to expose .startTime / .endTime as time objects),
    # matching ClassroomManagementTest.Course in the Java original.
    def __init__(self, id: int) -> None:
        self.id = id
        self.courses: List[Any] = []

    def addCourse(self, course: Any) -> None:
        # Java: if (!courses.contains(course)) { courses.add(course); }  -> uses equals()
        if course not in self.courses:
            self.courses.append(course)

    def removeCourse(self, course: Any) -> None:
        # Java List.remove(Object) removes the first equal element and is a
        # no-op when absent; Python list.remove raises ValueError if absent.
        try:
            self.courses.remove(course)
        except ValueError:
            pass

    def isFreeAt(self, checkTime: str) -> bool:
        # Java: LocalTime.parse(...) -> raises on bad input; time.fromisoformat
        # raises ValueError on bad input (both propagate an exception).
        t = time.fromisoformat(checkTime)
        for course in self.courses:
            # !time.isBefore(start) && !time.isAfter(end)  =>  start <= t <= end
            if not (t < course.startTime) and not (t > course.endTime):
                return False
        return True

    def checkCourseConflict(self, newCourse: Any) -> bool:
        newStartTime = newCourse.startTime
        newEndTime = newCourse.endTime

        for course in self.courses:
            # !(newEnd < c.start || newStart > c.end)  =>  inclusive overlap
            if not (newEndTime < course.startTime or newStartTime > course.endTime):
                return False
        return True