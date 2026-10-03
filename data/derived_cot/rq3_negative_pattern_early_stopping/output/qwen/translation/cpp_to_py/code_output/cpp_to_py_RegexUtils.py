import re


class RegexUtils:
    @staticmethod
    def match(pattern, text):
        return re.search(pattern, text) is not None

    @staticmethod
    def findall(pattern, text):
        return re.findall(pattern, text)

    @staticmethod
    def split(pattern, text):
        if not text:
            return []
        tokens = re.split(pattern, text)
        if tokens[0] != text:
            tokens.append('')
        return tokens

    @staticmethod
    def sub(pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    @staticmethod
    def generate_email_pattern():
        return r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    @staticmethod
    def generate_phone_number_pattern():
        return r'\b\d{3}-\d{3}-\d{4}\b'

    @staticmethod
    def generate_split_sentences_pattern():
        return r'(?<=[.!?])\s+(?=[A-Z])'

    @staticmethod
    def split_sentences(text):
        pattern = RegexUtils.generate_split_sentences_pattern()
        sentences = RegexUtils.split(pattern, text)
        if sentences and sentences[0] == '':
            sentences.pop(0)
        if sentences and sentences[-1] == '':
            sentences.pop()
        return sentences

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = RegexUtils.generate_phone_number_pattern()
        return RegexUtils.match(pattern, phone_number)

    @staticmethod
    def extract_email(text):
        pattern = RegexUtils.generate_email_pattern()
        return RegexUtils.findall(pattern, text)