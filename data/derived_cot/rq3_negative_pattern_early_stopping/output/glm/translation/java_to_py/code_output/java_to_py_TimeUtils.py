from datetime import datetime, timedelta

class TimeUtils:

    def __init__(self):
        self.datetime = datetime.now()

    def get_current_time(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_current_date(self):
        return self.datetime.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        new_datetime = self.datetime + timedelta(seconds=seconds)
        return new_datetime.strftime("%H:%M:%S")

    def string_to_datetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime_obj):
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        delta = time2 - time1
        total_seconds = delta.total_seconds()
        minutes = int(total_seconds // 60) if total_seconds >= 0 else -int((-total_seconds) // 60)
        if minutes < -2**31 or minutes > 2**31 - 1:
            raise OverflowError("integer overflow")
        return minutes

    def get_format_time(self, year, month, day, hour, minute, second):
        time_item = datetime(year, month, day, hour, minute, second)
        return time_item.strftime("%Y-%m-%d %H:%M:%S")