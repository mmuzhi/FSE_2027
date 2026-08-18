import re


class RegexUtils:

    def match(self, pattern, text):
        # Java's Matcher.matches() requires the entire region to match -> fullmatch
        return re.fullmatch(pattern, text) is not None

    def findall(self, pattern, text):
        # Java's matcher.group() is always group(0); Python findall would return
        # capture groups instead, so iterate matches and take group(0).
        return [m.group() for m in re.finditer(pattern, text)]

    def split(self, pattern, text):
        # Java's split(text, -1) keeps trailing empty strings; Python's re.split
        # retains them by default.
        return re.split(pattern, text)

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        return r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def generate_phone_number_pattern(self):
        return r"\b\d{3}-\d{3}-\d{4}\b"

    def generate_split_sentences_pattern(self):
        return r"[.!?][\s]{1,2}(?=[A-Z])"

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        return self.split(pattern, text)

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)