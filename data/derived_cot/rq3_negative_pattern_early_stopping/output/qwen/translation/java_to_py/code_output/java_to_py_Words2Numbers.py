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
        self.ordinal_words = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fifth": 5,
            "eighth": 8,
            "ninth": 9,
            "twelfth": 12
        }
        self.ordinal_endings = [
            ["ieth", "y"],
            ["th", ""]
        ]

        self._initialize_numwords()

    def _initialize_numwords(self):
        self.numwords["and"] = (1, 0)
        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)
        for idx, scale_word in enumerate(self.scales):
            exponent = 2 if idx == 0 else idx * 3
            self.numwords[scale_word] = (10 ** exponent, 0)

    def text2int(self, textnum):
        textnum = textnum.replace('-', ' ')
        words = textnum.split()

        current = 0
        result = 0
        curstring = []
        onnumber = False

        for word in words:
            if word in self.ordinal_words:
                scale = 1
                increment = self.ordinal_words[word]
                current = current * scale + increment
                onnumber = True
            else:
                for endings, replacement in self.ordinal_endings:
                    if word.endswith(endings[0]):
                        word = word[:-len(endings[0])] + replacement if replacement else word[:-len(endings[0])]
                if word not in self.numwords:
                    if onnumber:
                        curstring.append(str(result + current))
                    curstring.append(word)
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

        return ' '.join(curstring)

    def is_valid_input(self, textnum):
        textnum = textnum.replace('-', ' ')
        words = textnum.split()

        for word in words:
            normalized_word = word
            for endings, _ in self.ordinal_endings:
                if normalized_word.endswith(endings[0]):
                    normalized_word = normalized_word[:-len(endings[0])]
            if normalized_word not in self.numwords and word not in self.ordinal_words:
                return False
        return True