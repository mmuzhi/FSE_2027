import datetime
import sys
from typing import List, Tuple

class Course:
    def __init__(self, name: str, start_time: str, end_time: str):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return NotImplemented
        return (self.name == other.name and 
                self.start_time == other.start_time and 
                self.end_time == other.end_time)

    def __hash__(self) -> int:
        return hash((self.name, self.start_time, self.end_time))


class Classroom:
    def __init__(self, id: int):
        self.id = id
        self.courses: List[Course] = []

    def add_course(self, course: Course) -> None:
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course: Course) -> None:
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time: str) -> bool:
        check_dt = self._string_to_datetime(check_time)
        for course in self.courses:
            start_dt = self._string_to_datetime(course.start_time)
            end_dt = self._string_to_datetime(course.end_time)
            check_ts = check_dt.timestamp()
            start_ts = start_dt.timestamp()
            end_ts = end_dt.timestamp()
            if check_ts == -1 or start_ts == -1 or end_ts == -1:
                print("Time conversion failed", file=sys.stderr)
                return False
            if start_ts <= check_ts <= end_ts:
                return False
        return True

    def check_course_conflict(self, new_course: Course) -> bool:
        try:
            new_start_dt = self._string_to_datetime(new_course.start_time)
            new_end_dt = self._string_to_datetime(new_course.end_time)
        except ValueError:
            print("Time conversion failed", file=sys.stderr)
            return True
        for course in self.courses:
            try:
                start_dt = self._string_to_datetime(course.start_time)
                end_dt = self._string_to_datetime(course.end_time)
            except ValueError:
                print("Time conversion failed", file=sys.stderr)
                return True
            if self._is_time_conflict(start_dt, end_dt, new_start_dt, new_end_dt):
                return False
        return True

    def has_course(self, course: Course) -> bool:
        return course in self.courses

    def _string_to_datetime(self, time_str: str) -> datetime.datetime:
        try:
            parsed = datetime.datetime.strptime(time_str, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format: " + time_str)
        return parsed.replace(year=2020, month=1, day=1)

    def _is_time_conflict(self, start1: datetime.datetime, end1: datetime.datetime,
                          start2: datetime.datetime, end2: datetime.datetime) -> bool:
        t1_start = start1.timestamp()
        t1_end = end1.timestamp()
        t2_start = start2.timestamp()
        t2_end = end2.timestamp()
        return t1_start <= t2_end and t1_end >= t2_start