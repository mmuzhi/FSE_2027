class PersonRequest:
    def __init__(self, name, sex, phone_number):
        self.name = self.validate_name(name)
        self.sex = self.validate_sex(sex)
        self.phone_number = self.validate_phone_number(phone_number)

    @staticmethod
    def validate_name(name):
        if name is None or name == "" or len(name) > 33:
            return None
        return name

    @staticmethod
    def validate_sex(sex):
        if sex is None or sex not in ["Man", "Woman", "UGM"]:
            return None
        return sex

    @staticmethod
    def validate_phone_number(phone_number):
        if phone_number is None or phone_number == "" or len(phone_number) != 11 or not phone_number.isdigit():
            return None
        return phone_number

    def get_name(self):
        return self.name

    def get_sex(self):
        return self.sex

    def get_phone_number(self):
        return self.phone_number