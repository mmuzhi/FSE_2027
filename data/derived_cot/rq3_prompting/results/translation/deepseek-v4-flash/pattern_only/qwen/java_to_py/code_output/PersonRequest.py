import re

class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phoneNumber = self._validate_phone_number(phoneNumber)

    @staticmethod
    def _java_length(s):
        # Java String.length() counts UTF-16 code units.
        return len(s) + sum(1 for c in s if ord(c) > 0xFFFF)

    def _validate_name(self, name):
        if name is None or name == "" or self._java_length(name) > 33:
            return None
        return name

    def _validate_sex(self, sex):
        if sex is None or (sex != "Man" and sex != "Woman" and sex != "UGM"):
            return None
        return sex

    def _validate_phone_number(self, phoneNumber):
        if (
            phoneNumber is None
            or phoneNumber == ""
            or self._java_length(phoneNumber) != 11
            or re.fullmatch(r"[0-9]{11}", phoneNumber) is None
        ):
            return None
        return phoneNumber

    def getName(self):
        return self._name

    def getSex(self):
        return self._sex

    def getPhoneNumber(self):
        return self._phoneNumber