import re
from collections import defaultdict

class Words2Numbers:
    def __init__(self):
        self.numwords = {}
        self.units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                     "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                     "eighteen", "nineteen"]
        self.tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]
        self.ordinal_words = {"first": 1, "second": 2, "third": 3, "fifth": 5, "eighth": 8,
                             "ninth": 9, "twelfth": 12}
        self.ordinal_endings = [("ieth", "y"), ("th", "")]

        # Initialize numwords
        self.numwords["and"] = (1, 0)
        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)
        for idx, word in enumerate(self.scales):
            self.numwords[word] = (10**(idx * 3), 0)

    def text2int(self, textnum):
        # Replace hyphens with spaces and convert to lowercase
        text = textnum.replace('-', ' ')
        words = text.split()

        current = 0
        result = 0
        curstring = ""

        for word in words:
            # Check if it's an ordinal word
            if word in self.ordinal_words:
                scale = 1
                increment = self.ordinal_words[word]
                current = current * scale + increment
            else:
                # Process ordinal endings
                for suffix, replacement in self.ordinal_endings:
                    if len(word) > len(suffix) and word.endswith(suffix):
                        word = word[:-len(suffix)] + replacement

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
        text = textnum.replace('-', ' ')
        words = text.split()

        for word in words:
            if word in self.ordinal_words:
                continue
            # Process ordinal endings
            found_ending = False
            for suffix, replacement in self.ordinal_endings:
                if len(word) > len(suffix) and word.endswith(suffix):
                    word = word[:-len(suffix)] + replacement
                    found_ending = True
                    break

            if word not in self.numwords:
                return False

        return True