import re


def _expand_cpp_replacement(match, replacement):
    """Expand ECMAScript-style replacement strings used by C++ std::regex_replace."""
    out = []
    i = 0
    n = len(replacement)

    while i < n:
        c = replacement[i]
        if c != '$':
            out.append(c)
            i += 1
            continue

        if i + 1 >= n:
            out.append('$')
            i += 1
            continue

        nxt = replacement[i + 1]

        if nxt == '$':
            out.append('$')
            i += 2
        elif nxt == '&':
            out.append(match.group(0))
            i += 2
        elif nxt == '`':
            out.append(match.string[:match.start()])
            i += 2
        elif nxt == "'":
            out.append(match.string[match.end():])
            i += 2
        elif nxt.isdigit():
            j = i + 1
            while j < n and replacement[j].isdigit():
                j += 1
            digits = replacement[i + 1:j]

            if len(digits) >= 2:
                num = int(digits[:2])
                if 1 <= num <= 99 and num <= len(match.groups()):
                    val = match.group(num)
                    out.append('' if val is None else val)
                    i += 3
                    continue

            num = int(digits[0])
            if 1 <= num <= 9 and num <= len(match.groups()):
                val = match.group(num)
                out.append('' if val is None else val)
                i += 2
            else:
                out.append('$')
                i += 1
        else:
            out.append('$')
            i += 1

    return ''.join(out)


class RegexUtils:
    def match(self, pattern, text):
        return bool(re.search(pattern, text))

    def findall(self, pattern, text):
        return [m.group(0) for m in re.finditer(pattern, text)]

    def split(self, pattern, text):
        if text == "":
            return []

        matches = list(re.finditer(pattern, text))
        result = []
        prev = 0

        for m in matches:
            result.append(text[prev:m.start()])
            prev = m.end()

        result.append(text[prev:])

        if result[0] != text:
            result.append("")

        return result

    def sub(self, pattern, replacement, text):
        return re.sub(
            pattern,
            lambda m: _expand_cpp_replacement(m, replacement),
            text
        )

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