class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self.name = self.validate_name(name)
        self.sex = self.validate_sex(sex)
        self.phoneNumber = self.validate_phone_number(phoneNumber)
    
    def validate_name(self, name):
        if len(name) == 0 or len(name) > 33:
            return ""
        return name
    
    def validate_sex(self, sex):
        if sex not in ["Man", "Woman", "UGM"]:
            return ""
        return sex
    
    def validate_phone_number(self, phoneNumber):
        if len(phoneNumber) == 0 or len(phoneNumber) != 11 or not self.is_all_digits(phoneNumber):
            return ""
        return phoneNumber
    
    def is_all_digits(self, s):
        for char in s:
            if not char.isdigit():
                return False
        return True