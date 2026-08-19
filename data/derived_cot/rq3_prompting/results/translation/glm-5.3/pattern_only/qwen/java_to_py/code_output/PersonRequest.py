import re


class PersonRequest:
    def __init__(self, name, sex, phone_number):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phone_number = self._validate_phone_number(phone_number)

    @staticmethod
    def _validate_name(name):
        if name is None or name == "" or len(name) > 33:
            return None
        return name

    @staticmethod
    def _validate_sex(sex):
        if sex is None or (sex != "Man" and sex != "Woman" and sex != "UGM"):
            return None
        return sex

    @staticmethod
    def _validate_phone_number(phone_number):
        if (phone_number is None or phone_number == ""
                or len(phone_number) != 11
                or re.fullmatch(r"\d{11}", phone_number, re.ASCII) is None):
            return None
        return phone_number

    @property
    def name(self):
        return self._name

    @property
    def sex(self):
        return self._sex

    @property
    def phone_number(self):
        return self._phone_number