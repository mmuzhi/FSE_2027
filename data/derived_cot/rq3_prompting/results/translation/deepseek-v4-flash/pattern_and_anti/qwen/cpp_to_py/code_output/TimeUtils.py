import re
import time

class TimeUtils:
    def __init__(self):
        self.datetime = time.localtime()

    def get_current_time(self):
        return time.strftime("%H:%M:%S", self.datetime)

    def get_current_date(self):
        return time.strftime("%Y-%m-%d", self.datetime)

    def add_seconds(self, seconds):
        time_t_now = time.mktime(self.datetime)
        time_t_now += seconds
        new_datetime = time.localtime(time_t_now)
        self.datetime = new_datetime
        return time.strftime("%H:%M:%S", new_datetime)

    def string_to_datetime(self, s):
        m = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})\s*(\d{1,2}):(\d{1,2}):(\d{1,2})', s)
        if m:
            year, month, day, hour, minute, second = map(int, m.groups())
            return time.struct_time((year, month, day, hour, minute, second, 0, 1, 0))
        return time.struct_time((1900, 1, 0, 0, 0, 0, 0, 1, 0))

    def datetime_to_string(self, dt):
        return time.strftime("%Y-%m-%d %H:%M:%S", dt)

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        time_t1 = time.mktime(time1)
        time_t2 = time.mktime(time2)
        return int((time_t2 - time_t1) / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        tm = time.struct_time((year, month, day, hour, minute, second, 0, 1, 0))
        return time.strftime("%Y-%m-%d %H:%M:%S", tm)