class Words2Numbers:
    def __init__(self):
        self.units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
            "nineteen",
        ]

        self.tens = [
            "", "", "twenty", "thirty", "forty", "fifty", "sixty",
            "seventy", "eighty", "ninety",
        ]

        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]

        self.numwords = {"and": (1, 0)}
        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)
        for idx, word in enumerate(self.scales):
            self.numwords[word] = (10 ** (idx * 3), 0)
        self.numwords["hundred"] = (100, 0)

        self.ordinal_words = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fifth": 5,
            "eighth": 8,
            "ninth": 9,
            "twelfth": 12,
        }
        self.ordinal_endings = [("ieth", "y"), ("th", "")]

    def _apply_ordinal_endings(self, word):
        for ending, replacement in self.ordinal_endings:
            if len(word) > len(ending) and word.endswith(ending):
                word = word[: len(word) - len(ending)] + replacement
        return word

    def text2int(self, textnum):
        text = textnum.replace("-", " ")

        current = 0
        result = 0
        curstring = ""

        for word in text.split():
            if word in self.ordinal_words:
                current += self.ordinal_words[word]
            else:
                word = self._apply_ordinal_endings(word)

                if word not in self.numwords:
                    if current > 0:
                        result += current
                        current = 0
                    curstring += word + " "
                else:
                    scale, increment = self.numwords[word]
                    if scale == 1:
                        current += increment
                    else:
                        current *= scale
                        result += current
                        current = 0

        if current > 0:
            result += current

        curstring += str(result)
        return curstring

    def is_valid_input(self, textnum):
        text = textnum.replace("-", " ")

        for word in text.split():
            if word in self.ordinal_words:
                continue
            word = self._apply_ordinal_endings(word)
            if word not in self.numwords:
                return False

        return True