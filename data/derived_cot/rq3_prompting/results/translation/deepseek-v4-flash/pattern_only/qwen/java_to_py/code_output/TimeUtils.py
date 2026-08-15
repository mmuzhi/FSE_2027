from datetime import datetime, timedelta

class TimeUtils:
    def __init__(self):
        self.datetime = datetime.now()

    def getCurrentTime(self):
        return self.datetime.strftime("%H:%M:%S")

    def getCurrentDate(self):
        return self.datetime.strftime("%Y-%m-%d")

    def addSeconds(self, seconds):
        new_datetime = self.datetime + timedelta(seconds=seconds)
        return new_datetime.strftime("%H:%M:%S")

    def stringToDatetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetimeToString(self, datetime):
        return datetime.strftime("%Y-%m-%d %H:%M:%S")

    def getMinutes(self, stringTime1, stringTime2):
        time1 = self.stringToDatetime(stringTime1)
        time2 = self.stringToDatetime(stringTime2)
        minutes = int((time2 - time1).total_seconds() / 60)
        if minutes < -2147483648 or minutes > 2147483647:
            raise ArithmeticError("integer overflow")
        return minutes

    def getFormatTime(self, year, month, day, hour, minute, second):
        time_item = datetime(year, month, day, hour, minute, second)
        return time_item.strftime("%Y-%m-%d %H:%M:%S")