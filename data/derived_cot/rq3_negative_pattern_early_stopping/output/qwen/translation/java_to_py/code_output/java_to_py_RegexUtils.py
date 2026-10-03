import re


class RegexUtils:

    @staticmethod
    def match(pattern: str, text: str) -> bool:
        return re.fullmatch(pattern, text) is not None

    @staticmethod
    def findall(pattern: str, text: str) -> list[str]:
        return re.findall(pattern, text)

    @staticmethod
    def split(pattern: str, text: str) -> list[str]:
        return re.split(pattern, text)

    @staticmethod
    def sub(pattern: str, replacement: str, text: str) -> str:
        return re.sub(pattern, replacement, text)

    @staticmethod
    def generateEmailPattern() -> str:
        return r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    @staticmethod
    def generatePhoneNumberPattern() -> str:
        return r'\b\d{3}-\d{3}-\d{4}\b'

    @staticmethod
    def generateSplitSentencesPattern() -> str:
        return r'[.!?][\s]{1,2}(?=[A-Z])'

    @staticmethod
    def splitSentences(text: str) -> list[str]:
        pattern = RegexUtils.generateSplitSentencesPattern()
        return RegexUtils.split(pattern, text)

    @staticmethod
    def validatePhoneNumber(phoneNumber: str) -> bool:
        pattern = RegexUtils.generatePhoneNumberPattern()
        return RegexUtils.match(pattern, phoneNumber)

    @staticmethod
    def extractEmail(text: str) -> list[str]:
        pattern = RegexUtils.generateEmailPattern()
        return RegexUtils.findall(pattern, text)