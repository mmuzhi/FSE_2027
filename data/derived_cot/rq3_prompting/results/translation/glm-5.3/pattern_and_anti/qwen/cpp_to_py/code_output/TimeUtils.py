import time
from datetime import datetime, timedelta


class TimeUtils:
    def __init__(self):
        self.datetime = datetime.now()

    def get_current_time(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_current_date(self):
        return self.datetime.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        self.datetime += timedelta(seconds=seconds)
        return self.datetime.strftime("%H:%M:%S")

    def string_to_datetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime_):
        return datetime_.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        # C++ difftime(...)/60 assigned to int truncates toward zero
        return int((time2 - time1).total_seconds() / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        # struct_time mirrors std::tm: fields used as-is (no normalization by put_time)
        tm = time.struct_time((year, month, day, hour, minute, second, 0, 0, -1))
        return time.strftime("%Y-%m-%d %H:%M:%S", tm)