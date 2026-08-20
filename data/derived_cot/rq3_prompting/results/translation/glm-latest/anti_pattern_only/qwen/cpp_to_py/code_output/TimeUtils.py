import time


class TimeUtils:
    def __init__(self):
        # std::chrono::system_clock::now() -> time_t -> localtime
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
        # std::get_time leaves tm_wday/tm_yday/tm_isdst at their
        # zero-initialized values (mktime ignores wday/yday, uses isdst).
        return time.struct_time((tm.tm_year, tm.tm_mon, tm.tm_mday,
                                 tm.tm_hour, tm.tm_min, tm.tm_sec,
                                 0, 0, 0))

    def datetime_to_string(self, datetime):
        return time.strftime("%Y-%m-%d %H:%M:%S", datetime)

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)

        time_t1 = time.mktime(time1)
        time_t2 = time.mktime(time2)

        # difftime()/60 truncated toward zero, as in the C++ int conversion.
        return int((time_t2 - time_t1) / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        # time.strftime maps full year -> year-1900 and month -> month-1
        # internally, matching the C++ tm field assignments; wday/yday/isdst
        # remain zero-initialized and unused by this format.
        tm = (year, month, day, hour, minute, second, 0, 0, 0)
        return time.strftime("%Y-%m-%d %H:%M:%S", tm)