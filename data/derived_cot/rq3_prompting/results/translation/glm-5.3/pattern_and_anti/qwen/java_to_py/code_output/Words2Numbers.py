class Words2Numbers:

    def __init__(self):
        self.numwords = {}
        self.units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"
        ]
        self.tens = [
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        ]
        self.scales = [
            "hundred", "thousand", "million", "billion", "trillion"
        ]

        self.numwords["and"] = (1, 0)
        for idx in range(len(self.units)):
            self.numwords[self.units[idx]] = (1, idx)
        for idx in range(len(self.tens)):
            self.numwords[self.tens[idx]] = (1, idx * 10)
        for idx in range(len(self.scales)):
            self.numwords[self.scales[idx]] = (10 ** (2 if idx * 3 == 0 else idx * 3), 0)

        self.ordinalWords = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fifth": 5,
            "eighth": 8,
            "ninth": 9,
            "twelfth": 12,
        }

        self.ordinalEndings = [
            ("ieth", "y"), ("th", "")
        ]

    @staticmethod
    def _split(text):
        # Mimics Java's String.split(" "): drops trailing empty tokens,
        # but keeps at least one token (e.g. "" -> [""]).
        parts = text.split(" ")
        while len(parts) > 1 and parts[-1] == "":
            parts.pop()
        return parts

    def text2int(self, textnum):
        textnum = textnum.replace("-", " ")

        current = 0
        result = 0
        curstring = []
        onnumber = False

        for word in self._split(textnum):
            if word in self.ordinalWords:
                scale = 1
                increment = self.ordinalWords[word]
                current = current * scale + increment
                onnumber = True
            else:
                for ending in self.ordinalEndings:
                    if word.endswith(ending[0]):
                        word = word[:len(word) - len(ending[0])] + ending[1]

                if word not in self.numwords:
                    if onnumber:
                        curstring.append(str(result + current) + " ")
                    curstring.append(word + " ")
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = self.numwords[word]
                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True

        if onnumber:
            curstring.append(str(result + current))

        return "".join(curstring)

    def isValidInput(self, textnum):
        textnum = textnum.replace("-", " ")

        for word in self._split(textnum):
            if word in self.ordinalWords:
                continue
            else:
                for ending in self.ordinalEndings:
                    if word.endswith(ending[0]):
                        word = word[:len(word) - len(ending[0])] + ending[1]

                if word not in self.numwords:
                    return False

        return True