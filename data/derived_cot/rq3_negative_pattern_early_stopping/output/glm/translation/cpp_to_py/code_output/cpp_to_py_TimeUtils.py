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
        try:
            return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.min

    def datetime_to_string(self, datetime_obj):
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        diff = (time2 - time1).total_seconds()
        return int(diff / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"