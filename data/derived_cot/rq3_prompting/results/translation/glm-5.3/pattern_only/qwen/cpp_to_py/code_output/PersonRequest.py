class PersonRequest:
    def __init__(self, name, sex, phone_number):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phone_number = self._validate_phone_number(phone_number)

    def _validate_name(self, name):
        if len(name) == 0 or len(name) > 33:
            return ""
        return name

    def _validate_sex(self, sex):
        if sex != "Man" and sex != "Woman" and sex != "UGM":
            return ""
        return sex

    def _validate_phone_number(self, phone_number):
        if len(phone_number) == 0 or len(phone_number) != 11 or not self._is_all_digits(phone_number):
            return ""
        return phone_number

    def _is_all_digits(self, s):
        for c in s:
            if not ('0' <= c <= '9'):
                return False
        return True