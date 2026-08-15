import time


class Course:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return (self.name == other.name and
                self.start_time == other.start_time and
                self.end_time == other.end_time)


class Classroom:
    def __init__(self, id):
        self._id = id
        self._courses = []

    def add_course(self, course):
        new_course = Course(course.name, course.start_time, course.end_time)
        if new_course not in self._courses:
            self._courses.append(new_course)

    def remove_course(self, course):
        if course in self._courses:
            self._courses.remove(course)

    def is_free_at(self, check_time):
        check_tm = self._string_to_tm(check_time)
        for course in self._courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)
            check_tt = self._tm_to_time_t(check_tm)
            start_tt = self._tm_to_time_t(start_tm)
            end_tt = self._tm_to_time_t(end_tm)
            if check_tt >= start_tt and check_tt <= end_tt:
                return False
        return True

    def check_course_conflict(self, new_course):
        new_start_tm = self._string_to_tm(new_course.start_time)
        new_end_tm = self._string_to_tm(new_course.end_time)
        for course in self._courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)
            if self._is_time_conflict(start_tm, end_tm, new_start_tm, new_end_tm):
                return False
        return True

    def has_course(self, course):
        return course in self._courses

    def _string_to_tm(self, time_str):
        original = time_str
        time_str = time_str.lstrip(" \t\n\r\f\v")
        if len(time_str) < 5 or time_str[2] != ':':
            raise ValueError("Invalid time format: " + original)
        hour_str = time_str[0:2]
        minute_str = time_str[3:5]
        if not (all('0' <= c <= '9' for c in hour_str) and
                all('0' <= c <= '9' for c in minute_str)):
            raise ValueError("Invalid time format: " + original)
        hour = int(hour_str)
        minute = int(minute_str)
        if hour > 23 or minute > 59:
            raise ValueError("Invalid time format: " + original)
        return (2020, 1, 1, hour, minute, 0, 0, 1, 0)

    def _tm_to_time_t(self, tm):
        try:
            result = time.mktime(tm)
        except (OverflowError, OSError, ValueError):
            raise RuntimeError("Failed to convert std::tm to std::time_t")
        if result == -1:
            raise RuntimeError("Failed to convert std::tm to std::time_t")
        return int(result)

    def _is_time_conflict(self, start1, end1, start2, end2):
        t1_start = self._tm_to_time_t(start1)
        t1_end = self._tm_to_time_t(end1)
        t2_start = self._tm_to_time_t(start2)
        t2_end = self._tm_to_time_t(end2)
        return t1_start <= t2_end and t1_end >= t2_start