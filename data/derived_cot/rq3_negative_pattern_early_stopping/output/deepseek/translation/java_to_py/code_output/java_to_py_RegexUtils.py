import re

class RegexUtils:
    def match(self, pattern: str, text: str) -> bool:
        return bool(re.fullmatch(pattern, text))

    def findall(self, pattern: str, text: str) -> list:
        return [m.group() for m in re.finditer(pattern, text)]

    def split(self, pattern: str, text: str) -> list:
        return re.split(pattern, text)

    def sub(self, pattern: str, replacement: str, text: str) -> str:
        return re.sub(pattern, replacement, text)

    def generateEmailPattern(self) -> str:
        return r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def generatePhoneNumberPattern(self) -> str:
        return r"\b\d{3}-\d{3}-\d{4}\b"

    def generateSplitSentencesPattern(self) -> str:
        return r"[.!?][\s]{1,2}(?=[A-Z])"

    def splitSentences(self, text: str) -> list:
        pattern = self.generateSplitSentencesPattern()
        return self.split(pattern, text)

    def validatePhoneNumber(self, phoneNumber: str) -> bool:
        pattern = self.generatePhoneNumberPattern()
        return self.match(pattern, phoneNumber)

    def extractEmail(self, text: str) -> list:
        pattern = self.generateEmailPattern()
        return self.findall(pattern, text)