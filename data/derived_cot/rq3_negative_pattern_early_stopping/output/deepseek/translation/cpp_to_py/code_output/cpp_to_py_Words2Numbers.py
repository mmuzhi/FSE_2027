class Words2Numbers:
    def __init__(self):
        self.units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                      "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                      "eighteen", "nineteen"]
        self.tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]
        self.numwords = {}
        self.numwords["and"] = (1, 0)
        for idx, unit in enumerate(self.units):
            self.numwords[unit] = (1, idx)
        for idx, ten in enumerate(self.tens):
            self.numwords[ten] = (1, idx * 10)
        for idx, scale in enumerate(self.scales):
            self.numwords[scale] = (10 ** (idx * 3), 0)
        self.numwords["hundred"] = (100, 0)
        self.ordinal_words = {"first": 1, "second": 2, "third": 3, "fifth": 5, "eighth": 8,
                              "ninth": 9, "twelfth": 12}
        self.ordinal_endings = [("ieth", "y"), ("th", "")]

    def text2int(self, textnum: str) -> str:
        text = textnum.replace('-', ' ')
        current = 0
        result = 0
        curstring = ""
        for word in text.split():
            if word in self.ordinal_words:
                scale = 1
                increment = self.ordinal_words[word]
                current = current * scale + increment
            else:
                found_ending = False
                for ending, replacement in self.ordinal_endings:
                    if len(word) > len(ending) and word.endswith(ending):
                        word = word[:-len(ending)] + replacement
                        found_ending = True
                        break
                if word in self.numwords:
                    scale, increment = self.numwords[word]
                    if scale == 1:
                        current += increment
                    else:
                        current *= scale
                        result += current
                        current = 0
                else:
                    if current > 0:
                        result += current
                        current = 0
                    curstring += word + " "
        if current > 0:
            result += current
        curstring += str(result)
        return curstring

    def is_valid_input(self, textnum: str) -> bool:
        text = textnum.replace('-', ' ')
        for word in text.split():
            if word in self.ordinal_words:
                continue
            found_ending = False
            for ending, replacement in self.ordinal_endings:
                if len(word) > len(ending) and word.endswith(ending):
                    word = word[:-len(ending)] + replacement
                    found_ending = True
                    break
            if word not in self.numwords:
                return False
        return True