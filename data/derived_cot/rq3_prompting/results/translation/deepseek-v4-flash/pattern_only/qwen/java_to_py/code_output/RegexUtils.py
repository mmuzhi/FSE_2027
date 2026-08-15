import re


class RegexUtils:
    def match(self, pattern, text):
        return re.fullmatch(pattern, text) is not None

    def findall(self, pattern, text):
        return [m.group() for m in re.finditer(pattern, text)]

    def split(self, pattern, text):
        result = []
        last = 0
        for m in re.finditer(pattern, text):
            result.append(text[last:m.start()])
            last = m.end()
        result.append(text[last:])
        return result

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, lambda m: self._java_replace(m, replacement), text)

    def generateEmailPattern(self):
        return r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def generatePhoneNumberPattern(self):
        return r"\b\d{3}-\d{3}-\d{4}\b"

    def generateSplitSentencesPattern(self):
        return r"[.!?][\s]{1,2}(?=[A-Z])"

    def splitSentences(self, text):
        pattern = self.generateSplitSentencesPattern()
        return self.split(pattern, text)

    def validatePhoneNumber(self, phoneNumber):
        pattern = self.generatePhoneNumberPattern()
        return self.match(pattern, phoneNumber)

    def extractEmail(self, text):
        pattern = self.generateEmailPattern()
        return self.findall(pattern, text)

    def _java_replace(self, match, template):
        result = []
        i = 0
        n = len(template)

        while i < n:
            c = template[i]

            if c == '\\':
                if i + 1 < n:
                    result.append(template[i + 1])
                    i += 2
                else:
                    result.append('\\')
                    i += 1

            elif c == '$':
                if i + 1 < n and template[i + 1].isdigit():
                    j = i + 1
                    while j < n and template[j].isdigit():
                        j += 1
                    num = int(template[i + 1:j])
                    group = match.group(num)
                    result.append(group if group is not None else '')
                    i = j

                elif i + 1 < n and template[i + 1] == '{':
                    end = template.find('}', i + 2)
                    if end == -1:
                        raise ValueError("named capturing group is missing trailing '}'")
                    name = template[i + 2:end]
                    if name not in match.re.groupindex:
                        raise ValueError("No group with name " + name)
                    group = match.group(name)
                    result.append(group if group is not None else '')
                    i = end + 1

                else:
                    result.append('$')
                    i += 1

            else:
                result.append(c)
                i += 1

        return ''.join(result)