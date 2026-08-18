from datetime import datetime, timedelta


class TimeUtils:

    def __init__(self):
        self.datetime = datetime.now()

    def get_current_time(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_current_date(self):
        return "{:04d}-{:02d}-{:02d}".format(
            self.datetime.year, self.datetime.month, self.datetime.day
        )

    def add_seconds(self, seconds):
        new_datetime = self.datetime + timedelta(seconds=seconds)
        return new_datetime.strftime("%H:%M:%S")

    def string_to_datetime(self, string):
        # Java pattern "yyyy-M-d H:m:s" accepts non-zero-padded fields;
        # strptime's %Y-%m-%d %H:%M:%S also accepts 1-2 digit fields.
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, dt):
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second,
        )

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        # ChronoUnit.MINUTES.between truncates toward zero (complete minutes),
        # then Math.round/Math.toIntExact are identity for a long -> int().
        seconds = int((time2 - time1).total_seconds())
        return int(seconds / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        time_item = datetime(year, month, day, hour, minute, second)
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            time_item.year, time_item.month, time_item.day,
            time_item.hour, time_item.minute, time_item.second,
        )