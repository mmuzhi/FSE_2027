import time


class TimeUtils:
    def __init__(self):
        # Snapshot of current local time, stored as the object's state (std::tm analog).
        self.datetime = time.localtime()

    def get_current_time(self):
        return time.strftime("%H:%M:%S", self.datetime)

    def get_current_date(self):
        return time.strftime("%Y-%m-%d", self.datetime)

    def add_seconds(self, seconds):
        time_t_now = time.mktime(self.datetime)
        time_t_now += seconds
        self.datetime = time.localtime(time_t_now)
        return time.strftime("%H:%M:%S", self.datetime)

    def string_to_datetime(self, str):
        tm = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        # C++ zero-initializes std::tm (tm_isdst = 0); strptime yields isdst = -1.
        return time.struct_time(tm[:8] + (0,))

    def datetime_to_string(self, datetime):
        return time.strftime("%Y-%m-%d %H:%M:%S", datetime)

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)

        time_t1 = time.mktime(time1)
        time_t2 = time.mktime(time2)

        # difftime()/60 truncated to int -> truncate toward zero (not floor).
        return int((time_t2 - time_t1) / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        # std::tm tm = {} equivalent: weekday/yday/isdst zeroed, no normalization.
        tm = time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        return time.strftime("%Y-%m-%d %H:%M:%S", tm)