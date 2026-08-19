from datetime import datetime, timedelta


class TimeUtils:

    def __init__(self):
        self.datetime = datetime.now()

    def get_current_time(self):
        return f"{self.datetime.hour:02d}:{self.datetime.minute:02d}:{self.datetime.second:02d}"

    def get_current_date(self):
        return f"{self.datetime.year:04d}-{self.datetime.month:02d}-{self.datetime.day:02d}"

    def add_seconds(self, seconds):
        new_datetime = self.datetime + timedelta(seconds=seconds)
        return f"{new_datetime.hour:02d}:{new_datetime.minute:02d}:{new_datetime.second:02d}"

    def string_to_datetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, dt):
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        delta = time2 - time1
        # Java's ChronoUnit.MINUTES.between truncates toward zero; Python's // floors.
        total_seconds = delta.days * 86400 + delta.seconds
        sign = -1 if total_seconds < 0 else 1
        return sign * (abs(total_seconds) // 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        time_item = datetime(year, month, day, hour, minute, second)
        return self.datetime_to_string(time_item)