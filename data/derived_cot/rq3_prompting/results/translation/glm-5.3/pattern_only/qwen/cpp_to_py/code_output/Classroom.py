import re
import sys
import time
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    start_time: str
    end_time: str


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

        for course in self.courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)
            check_tt = self._tm_to_time_t(check_tm)
            start_tt = self._tm_to_time_t(start_tm)
            end_tt = self._tm_to_time_t(end_tm)

            if check_tt == -1 or start_tt == -1 or end_tt == -1:
                print("Time conversion failed", file=sys.stderr)
                return False

            if start_tt <= check_tt <= end_tt:
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
        # Mimics std::get_time(&tm, "%H:%M"): anchored parse of 1-2 digit
        # hour/minute, trailing characters ignored, range-checked.
        m = re.match(r'\s*(\d{1,2}):(\d{1,2})', time_str)
        if m is None:
            raise ValueError("Invalid time format: " + time_str)
        hour = int(m.group(1))
        minute = int(m.group(2))
        if hour > 23 or minute > 59:
            raise ValueError("Invalid time format: " + time_str)

        # tm_year = 120 (2020), tm_mon = 0 (January), tm_mday = 1, isdst = 0
        return time.struct_time((120, 0, 1, hour, minute, 0, 0, 0, 0))

    def _tm_to_time_t(self, tm):
        tt = time.mktime(tm)

        if tt == -1:
            raise RuntimeError("Failed to convert std::tm to std::time_t")

        return tt

    def _is_time_conflict(self, start1, end1, start2, end2):
        t1_start = self._tm_to_time_t(start1)
        t1_end = self._tm_to_time_t(end1)
        t2_start = self._tm_to_time_t(start2)
        t2_end = self._tm_to_time_t(end2)

        return t1_start <= t2_end and t1_end >= t2_start