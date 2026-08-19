from datetime import time


class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        # Java's List.remove silently does nothing when absent;
        # Python's list.remove would raise ValueError, so guard it.
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        t = time.fromisoformat(check_time)
        for course in self.courses:
            # Equivalent to: !t.isBefore(start) && !t.isAfter(end)
            if course.start_time <= t <= course.end_time:
                return False
        return True

    def check_course_conflict(self, new_course):
        new_start_time = new_course.start_time
        new_end_time = new_course.end_time

        for course in self.courses:
            # Equivalent to: !(newEnd.isBefore(c.start) || newStart.isAfter(c.end))
            if not (new_end_time < course.start_time or new_start_time > course.end_time):
                return False
        return True