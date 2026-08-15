import re

class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phoneNumber = self._validate_phone_number(phoneNumber)

    @staticmethod
    def _utf16_length(s):
        return len(s.encode('utf-16-le', errors='surrogatepass')) // 2

    @staticmethod
    def _validate_name(name):
        if name is None or name == "" or PersonRequest._utf16_length(name) > 33:
            return None
        return name

    @staticmethod
    def _validate_sex(sex):
        if sex is None or sex not in ("Man", "Woman", "UGM"):
            return None
        return sex

    @staticmethod
    def _validate_phone_number(phoneNumber):
        if phoneNumber is None or phoneNumber == "" or PersonRequest._utf16_length(phoneNumber) != 11 or not re.fullmatch(r"[0-9]{11}", phoneNumber):
            return None
        return phoneNumber

    def getName(self):
        return self._name

    def getSex(self):
        return self._sex

    def getPhoneNumber(self):
        return self._phoneNumber