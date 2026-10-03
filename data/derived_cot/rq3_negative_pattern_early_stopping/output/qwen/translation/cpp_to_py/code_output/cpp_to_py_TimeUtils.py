import time
import datetime

class TimeUtils:
    def __init__(self):
        # Get current time in UTC and convert to local time
        now = time.time()
        self.datetime = time.localtime(now)

    def get_current_time(self) -> str:
        return time.strftime("%H:%M:%S", self.datetime)

    def get_current_date(self) -> str:
        return time.strftime("%Y-%m-%d", self.datetime)

    def add_seconds(self, seconds: int) -> str:
        # Convert struct_time to seconds since epoch
        timestamp = time.mktime(self.datetime)
        new_timestamp = timestamp + seconds
        # Convert back to struct_time
        new_datetime = time.localtime(new_timestamp)
        self.datetime = new_datetime
        return time.strftime("%H:%M:%S", new_datetime)

    def string_to_datetime(self, str_time: str) -> time.struct_time:
        return time.strptime(str_time, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime_struct: time.struct_time) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", datetime_struct)

    def get_minutes(self, string_time1: str, string_time2: str) -> int:
        dt1 = time.strptime(string_time1, "%Y-%m-%d %H:%M:%S")
        dt2 = time.strptime(string_time2, "%Y-%m-%d %H:%M:%S")
        # Convert to timestamp (seconds since epoch)
        t1 = time.mktime(dt1)
        t2 = time.mktime(dt2)
        # difftime returns double (seconds) difference, then convert to minutes
        return int((t2 - t1) / 60)

    def get_format_time(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> str:
        # Create a struct_time with the given values
        # Note: struct_time uses (year, month, day, hour, minute, second, weekday, Julian day, DST)
        # We don't need all fields, but we have to create a tuple with the correct order.
        # We'll create a tuple and then convert to struct_time.
        # Alternatively, we can use time.struct_time directly.
        dt = time.struct_time((year, month, day, hour, minute, second, -1, -1, -1))
        return time.strftime("%Y-%m-%d %H:%M:%S", dt)