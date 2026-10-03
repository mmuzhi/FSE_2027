from datetime import time


class Classroom:
    def __init__(self, id: int):
        self.id = id
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        try:
            self.courses.remove(course)
        except ValueError:
            pass

    def is_free_at(self, check_time: str) -> bool:
        t = time.fromisoformat(check_time)
        for course in self.courses:
            if not (t < course.start_time) and not (t > course.end_time):
                return False
        return True

    def check_course_conflict(self, new_course) -> bool:
        new_start_time = new_course.start_time
        new_end_time = new_course.end_time

        for course in self.courses:
            if not (new_end_time < course.start_time or new_start_time > course.end_time):
                return False
        return True