class PersonRequest:
    def __init__(self, name: str, sex: str, phoneNumber: str):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phoneNumber = self._validate_phone_number(phoneNumber)

    def _validate_name(self, name):
        if name == "" or len(name) > 33:
            return ""
        return name

    def _validate_sex(self, sex):
        if sex != "Man" and sex != "Woman" and sex != "UGM":
            return ""
        return sex

    def _validate_phone_number(self, phoneNumber):
        if phoneNumber == "" or len(phoneNumber) != 11 or not self._is_all_digits(phoneNumber):
            return ""
        return phoneNumber

    def _is_all_digits(self, s):
        for c in s:
            if not ('0' <= c <= '9'):
                return False
        return True