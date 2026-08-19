import re


class RegexUtils:
    def match(self, pattern, text):
        # C++ uses std::regex_search (unanchored), so re.search, not re.match
        return re.search(pattern, text) is not None

    def findall(self, pattern, text):
        # Mirrors sregex_iterator + i->str(): collect full (group 0) matches
        return [m.group(0) for m in re.finditer(pattern, text)]

    def split(self, pattern, text):
        result = re.split(pattern, text)
        if text == "":
            return result
        if result[0] != text:
            result.append("")
        return result

    def sub(self, pattern, replacement, text):
        # std::regex_replace replaces all occurrences by default
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        return r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def generate_phone_number_pattern(self):
        return r"\b\d{3}-\d{3}-\d{4}\b"

    def generate_split_sentences_pattern(self):
        return r"[.!?][\s]{1,2}(?=[A-Z])"

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        sentences = self.split(pattern, text)

        if sentences and sentences[0] == "":
            sentences.pop(0)
        if sentences and sentences[-1] == "":
            sentences.pop()

        return sentences

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)