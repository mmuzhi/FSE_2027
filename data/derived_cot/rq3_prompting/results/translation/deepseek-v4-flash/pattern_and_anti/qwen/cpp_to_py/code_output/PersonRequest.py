class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phoneNumber = self._validate_phone_number(phoneNumber)

    def _validate_name(self, name):
        if not name or len(name) > 33:
            return ""
        return name

    def _validate_sex(self, sex):
        if sex not in ("Man", "Woman", "UGM"):
            return ""
        return sex

    def _validate_phone_number(self, phoneNumber):
        if not phoneNumber or len(phoneNumber) != 11 or not self._is_all_digits(phoneNumber):
            return ""
        return phoneNumber

    def _is_all_digits(self, s):
        return all('0' <= c <= '9' for c in s)