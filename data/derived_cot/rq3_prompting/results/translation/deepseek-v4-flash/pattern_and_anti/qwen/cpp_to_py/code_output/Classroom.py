import time
from datetime import datetime


class Course:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return (self.name == other.name and
                self.start_time == other.start_time and
                self.end_time == other.end_time)


class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        check_tm = self._string_to_tm(check_time)
        check_tt = self._tm_to_time_t(check_tm)

        for course in self.courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)
            start_tt = self._tm_to_time_t(start_tm)
            end_tt = self._tm_to_time_t(end_tm)

            if check_tt >= start_tt and check_tt <= end_tt:
                return False

        return True

    def check_course_conflict(self, new_course):
        new_start_tm = self._string_to_tm(new_course.start_time)
        new_end_tm = self._string_to_tm(new_course.end_time)

        for course in self.courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)

            if self._is_time_conflict(start_tm, end_tm, new_start_tm, new_end_tm):
                return False

        return True

    def has_course(self, course):
        return course in self.courses

    def _string_to_tm(self, time_str):
        try:
            dt = datetime.strptime(time_str, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format: " + time_str)
        return dt.replace(year=2020, month=1, day=1)

    def _tm_to_time_t(self, tm):
        try:
            result = time.mktime(
                (tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, 0, 0, 0)
            )
        except (OverflowError, ValueError):
            raise RuntimeError("Failed to convert std::tm to std::time_t")

        if result == -1:
            raise RuntimeError("Failed to convert std::tm to std::time_t")

        return result

    def _is_time_conflict(self, start1, end1, start2, end2):
        t1_start = self._tm_to_time_t(start1)
        t1_end = self._tm_to_time_t(end1)
        t2_start = self._tm_to_time_t(start2)
        t2_end = self._tm_to_time_t(end2)

        return t1_start <= t2_end and t1_end >= t2_start