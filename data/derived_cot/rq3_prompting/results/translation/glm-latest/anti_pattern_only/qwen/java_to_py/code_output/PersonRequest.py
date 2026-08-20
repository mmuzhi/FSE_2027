import re


def _utf16_length(s):
    # Java's String.length() counts UTF-16 code units, so characters
    # outside the BMP (e.g. most emoji) count as 2.
    return sum(2 if ord(ch) > 0xFFFF else 1 for ch in s)


class PersonRequest:
    def __init__(self, name, sex, phone_number):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phone_number = self._validate_phone_number(phone_number)

    def _validate_name(self, name):
        if name is None or name == "" or _utf16_length(name) > 33:
            return None
        return name

    def _validate_sex(self, sex):
        if sex is None or sex not in ("Man", "Woman", "UGM"):
            return None
        return sex

    def _validate_phone_number(self, phone_number):
        if (
            phone_number is None
            or phone_number == ""
            or _utf16_length(phone_number) != 11
            or re.fullmatch(r"\d{11}", phone_number, flags=re.ASCII) is None
        ):
            return None
        return phone_number

    def get_name(self):
        return self._name

    def get_sex(self):
        return self._sex

    def get_phone_number(self):
        return self._phone_number