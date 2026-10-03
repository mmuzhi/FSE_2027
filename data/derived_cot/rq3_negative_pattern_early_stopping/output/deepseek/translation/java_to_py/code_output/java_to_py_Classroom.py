from datetime import time, datetime
from typing import List

class Course:
    def __init__(self, start_time: time, end_time: time):
        self.start_time = start_time
        self.end_time = end_time

class Classroom:
    def __init__(self, id: int):
        self.id = id
        self.courses: List[Course] = []

    def addCourse(self, course: Course) -> None:
        if course not in self.courses:
            self.courses.append(course)

    def removeCourse(self, course: Course) -> None:
        if course in self.courses:
            self.courses.remove(course)

    def isFreeAt(self, checkTime: str) -> bool:
        time_obj = datetime.strptime(checkTime, "%H:%M").time()
        for course in self.courses:
            if not (time_obj < course.start_time) and not (time_obj > course.end_time):
                return False
        return True

    def checkCourseConflict(self, newCourse: Course) -> bool:
        new_start = newCourse.start_time
        new_end = newCourse.end_time
        for course in self.courses:
            if not (new_end < course.start_time or new_start > course.end_time):
                return False
        return True