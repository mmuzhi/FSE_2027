import re
from typing import Optional

class PersonRequest:
    def __init__(self, name: Optional[str], sex: Optional[str], phone_number: Optional[str]):
        self._name = self._validate_name(name)
        self._sex = self._validate_sex(sex)
        self._phone_number = self._validate_phone_number(phone_number)

    @staticmethod
    def _validate_name(name: Optional[str]) -> Optional[str]:
        if name is None or name == "" or len(name) > 33:
            return None
        return name

    @staticmethod
    def _validate_sex(sex: Optional[str]) -> Optional[str]:
        if sex is None or sex not in ("Man", "Woman", "UGM"):
            return None
        return sex

    @staticmethod
    def _validate_phone_number(phone_number: Optional[str]) -> Optional[str]:
        if phone_number is None or phone_number == "" or len(phone_number) != 11 or not re.fullmatch(r"\d{11}", phone_number):
            return None
        return phone_number

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def sex(self) -> Optional[str]:
        return self._sex

    @property
    def phone_number(self) -> Optional[str]:
        return self._phone_number