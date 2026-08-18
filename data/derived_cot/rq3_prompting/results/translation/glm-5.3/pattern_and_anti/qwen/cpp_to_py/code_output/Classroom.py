import re
import sys
import time
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    start_time: str
    end_time: str


# Mirrors std::get_time(&tm, "%H:%M"): parses 1-2 digits for hour/minute,
# accepts trailing garbage, fails on out-of-range values.
_TIME_PATTERN = re.compile(r"(\d{1,2}):(\d{1,2})")


class Classroom:
    def __init__(self, id: int):
        self._id = id
        self._courses = []

    def add_course(self, course: Course) -> None:
        if course not in self._courses:
            self._courses.append(course)

    def remove_course(self, course: Course) -> None:
        if course in self._courses:
            self._courses.remove(course)

    def is_free_at(self, check_time: str) -> bool:
        check_tm = self._string_to_tm(check_time)

        for course in self._courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)
            check_tt = self._tm_to_time_t(check_tm)
            start_tt = self._tm_to_time_t(start_tm)
            end_tt = self._tm_to_time_t(end_tm)

            if check_tt == -1 or start_tt == -1 or end_tt == -1:
                print("Time conversion failed", file=sys.stderr, flush=True)
                return False

            if start_tt <= check_tt <= end_tt:
                return False
        return True

    def check_course_conflict(self, new_course: Course) -> bool:
        new_start_tm = self._string_to_tm(new_course.start_time)
        new_end_tm = self._string_to_tm(new_course.end_time)

        if new_start_tm.tm_hour == -1 or new_end_tm.tm_hour == -1:
            print("Time conversion failed", file=sys.stderr, flush=True)
            return True

        for course in self._courses:
            start_tm = self._string_to_tm(course.start_time)
            end_tm = self._string_to_tm(course.end_time)

            if start_tm.tm_hour == -1 or end_tm.tm_hour == -1:
                print("Time conversion failed", file=sys.stderr, flush=True)
                return True

            if self._is_time_conflict(start_tm, end_tm, new_start_tm, new_end_tm):
                return False
        return True

    def has_course(self, course: Course) -> bool:
        return course in self._courses

    def _string_to_tm(self, time_str: str) -> time.struct_time:
        match = _TIME_PATTERN.match(time_str)
        if match is None:
            raise ValueError("Invalid time format: " + time_str)

        tm_hour = int(match.group(1))
        tm_min = int(match.group(2))
        if not (0 <= tm_hour <= 23) or not (0 <= tm_min <= 59):
            raise ValueError("Invalid time format: " + time_str)

        # tm_year = 120 (i.e. 2020), tm_mon = 0 (January), tm_mday = 1, tm_isdst = 0
        return time.struct_time((120 + 1900, 0 + 1, 1, tm_hour, tm_min, 0, 0, 0, 0))

    def _tm_to_time_t(self, tm: time.struct_time) -> float:
        try:
            time_tt = time.mktime(tm)
        except (OverflowError, ValueError):
            raise RuntimeError("Failed to convert std::tm to std::time_t")

        if time_tt == -1:
            raise RuntimeError("Failed to convert std::tm to std::time_t")

        return time_tt

    def _is_time_conflict(self, start1, end1, start2, end2) -> bool:
        t1_start = self._tm_to_time_t(start1)
        t1_end = self._tm_to_time_t(end1)
        t2_start = self._tm_to_time_t(start2)
        t2_end = self._tm_to_time_t(end2)

        return t1_start <= t2_end and t1_end >= t2_start