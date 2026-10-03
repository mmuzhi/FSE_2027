import datetime
import math


class TimeUtils:
    def __init__(self):
        self.datetime = datetime.datetime.now()

    def getCurrentTime(self):
        return self.datetime.strftime("%H:%M:%S")

    def getCurrentDate(self):
        return self.datetime.strftime("%Y-%m-%d")

    def addSeconds(self, seconds):
        new_datetime = self.datetime + datetime.timedelta(seconds=seconds)
        return new_datetime.strftime("%H:%M:%S")

    def stringToDatetime(self, string):
        parts = string.split(' ')
        if len(parts) != 2:
            raise ValueError("Invalid datetime string format")
        date_part = parts[0]
        time_part = parts[1]
        date_components = date_part.split('-')
        time_components = time_part.split(':')
        if len(date_components) != 3 or len(time_components) != 3:
            raise ValueError("Invalid datetime string format")
        year = int(date_components[0])
        month = int(date_components[1])
        day = int(date_components[2])
        hour = int(time_components[0])
        minute = int(time_components[1])
        second = int(time_components[2])
        return datetime.datetime(year, month, day, hour, minute, second)

    def datetimeToString(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def getMinutes(self, stringTime1, stringTime2):
        time1 = self.stringToDatetime(stringTime1)
        time2 = self.stringToDatetime(stringTime2)
        diff_seconds = (time2 - time1).total_seconds()
        minutes = diff_seconds / 60.0
        rounded = int(math.floor(minutes + 0.5))
        return rounded

    def getFormatTime(self, year, month, day, hour, minute, second):
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        return time_item.strftime("%Y-%m-%d %H:%M:%S")