import time
from datetime import datetime

class Course:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return (self.name == other.name and 
                self.start_time == other.start_time and 
                self.end_time == other.end_time)

class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def add_course(self, course):
        if not self.has_course(course):
            self.courses.append(course)

    def remove_course(self, course):
        if self.has_course(course):
            self.courses.remove(course)

    def is_free_at(self, check_time):
        try:
            check_timestamp = self.time_str_to_timestamp(check_time)
        except ValueError:
            return False

        for course in self.courses:
            try:
                start_timestamp = self.time_str_to_timestamp(course.start_time)
                end_timestamp = self.time_str_to_timestamp(course.end_time)
            except ValueError:
                continue

            if check_timestamp >= start_timestamp and check_timestamp <= end_timestamp:
                return False
        return True

    def check_course_conflict(self, new_course):
        try:
            new_start_timestamp = self.time_str_to_timestamp(new_course.start_time)
            new_end_timestamp = self.time_str_to_timestamp(new_course.end_time)
        except ValueError:
            return True

        for course in self.courses:
            try:
                start_timestamp = self.time_str_to_timestamp(course.start_time)
                end_timestamp = self.time_str_to_timestamp(course.end_time)
            except ValueError:
                continue

            if self.is_time_conflict(start_timestamp, end_timestamp, new_start_timestamp, new_end_timestamp):
                return False
        return True

    def has_course(self, course):
        for existing_course in self.courses:
            if existing_course == course:
                return True
        return False

    def is_time_conflict(self, t1_start, t1_end, t2_start, t2_end):
        return (t1_start <= t2_end and t1_end >= t2_start)

    def time_str_to_timestamp(self, time_str):
        try:
            dt = datetime.strptime(time_str, "%H:%M")
            fixed_date = datetime(2000, 1, 1, dt.hour, dt.minute, 0)
            return time.mktime(fixed_date.timetuple())
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}")