import re

class RegexUtils:
    def match(self, pattern, text):
        return re.search(pattern, text) is not None

    def findall(self, pattern, text):
        return [m.group(0) for m in re.finditer(pattern, text)]

    def split(self, pattern, text):
        result = self._tokenize_unmatched(pattern, text)
        if text == "":
            return result
        if result[0] != text:
            result.append("")
        return result

    def _tokenize_unmatched(self, pattern, text):
        matches = list(re.finditer(pattern, text))
        result = []
        pos = 0
        for m in matches:
            result.append(text[pos:m.start()])
            pos = m.end()
        result.append(text[pos:])
        return result

    def sub(self, pattern, replacement, text):
        regex = re.compile(pattern)

        def repl(m):
            return self._format_replacement(m, replacement, text)

        return regex.sub(repl, text)

    def _format_replacement(self, match, replacement, text):
        result = []
        i = 0
        n = len(replacement)
        while i < n:
            c = replacement[i]
            if c == '$' and i + 1 < n:
                nxt = replacement[i + 1]
                if nxt == '$':
                    result.append('$')
                    i += 2
                elif nxt == '&':
                    result.append(match.group(0))
                    i += 2
                elif nxt == '`':
                    result.append(text[:match.start()])
                    i += 2
                elif nxt == "'":
                    result.append(text[match.end():])
                    i += 2
                elif nxt.isdigit():
                    j = i + 1
                    num_str = ''
                    while j < n and replacement[j].isdigit() and len(num_str) < 2:
                        num_str += replacement[j]
                        j += 1
                    group_num = int(num_str)
                    if group_num == 0:
                        result.append('$' + num_str)
                    else:
                        try:
                            group = match.group(group_num)
                            result.append(group if group is not None else '')
                        except IndexError:
                            result.append('$' + num_str)
                    i = j
                else:
                    result.append('$')
                    i += 1
            else:
                result.append(c)
                i += 1
        return ''.join(result)

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