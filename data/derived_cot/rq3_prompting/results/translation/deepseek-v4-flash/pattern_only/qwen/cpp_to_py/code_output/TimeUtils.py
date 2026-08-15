import time

class TimeUtils:
    def __init__(self):
        self.datetime = time.localtime()

    def get_current_time(self):
        return time.strftime("%H:%M:%S", self.datetime)

    def get_current_date(self):
        return time.strftime("%Y-%m-%d", self.datetime)

    def add_seconds(self, seconds):
        seconds = int(seconds)
        time_t_now = time.mktime(self.datetime)
        time_t_now += seconds
        new_datetime = time.localtime(time_t_now)
        self.datetime = new_datetime
        return time.strftime("%H:%M:%S", new_datetime)

    def string_to_datetime(self, s):
        def is_digit(c):
            return '0' <= c <= '9'

        def is_space(c):
            return c in ' \t\n\r\v\f'

        def read_int(pos, max_digits):
            start = pos
            while pos < len(s) and is_digit(s[pos]) and pos - start < max_digits:
                pos += 1
            if pos == start:
                return None, pos
            return int(s[start:pos]), pos

        pos = 0
        while pos < len(s) and is_space(s[pos]):
            pos += 1

        year, month, day = 1900, 1, 0
        hour = minute = second = 0

        if pos + 4 <= len(s) and all(is_digit(c) for c in s[pos:pos + 4]):
            year = int(s[pos:pos + 4])
            pos += 4
        else:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))

        if pos >= len(s) or s[pos] != '-':
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        pos += 1

        val, pos = read_int(pos, 2)
        if val is None:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        month = val

        if pos >= len(s) or s[pos] != '-':
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        pos += 1

        val, pos = read_int(pos, 2)
        if val is None:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        day = val

        while pos < len(s) and is_space(s[pos]):
            pos += 1

        val, pos = read_int(pos, 2)
        if val is None:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        hour = val

        if pos >= len(s) or s[pos] != ':':
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        pos += 1

        val, pos = read_int(pos, 2)
        if val is None:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        minute = val

        if pos >= len(s) or s[pos] != ':':
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        pos += 1

        val, pos = read_int(pos, 2)
        if val is None:
            return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        second = val

        return time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))

    def datetime_to_string(self, dt):
        return time.strftime("%Y-%m-%d %H:%M:%S", dt)

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        time_t1 = time.mktime(time1)
        time_t2 = time.mktime(time2)
        return int((time_t2 - time_t1) / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        tm = time.struct_time((year, month, day, hour, minute, second, 0, 0, 0))
        return time.strftime("%Y-%m-%d %H:%M:%S", tm)