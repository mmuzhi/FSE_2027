import re

class PersonRequest:
    def __init__(self, name: str, sex: str, phone_number: str):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phone_number = self._validate_phone_number(phone_number)

    def _validate_name(self, name: str):
        if name is None or name == "" or len(name) > 33:
            return None
        return name

    def _validate_sex(self, sex: str):
        if sex is None or sex not in ("Man", "Woman", "UGM"):
            return None
        return sex

    def _validate_phone_number(self, phone_number: str):
        if phone_number is None or phone_number == "" or len(phone_number) != 11:
            return None
        if not re.fullmatch(r"\d{11}", phone_number):
            return None
        return phone_number

    def get_name(self):
        return self._name

    def get_sex(self):
        return self._sex

    def get_phone_number(self):
        return self._phone_number