class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_units = self._utf16_units(text)
        self.pattern_units = self._utf16_units(pattern)
        self.textLen = len(self.text_units)
        self.patLen = len(self.pattern_units)

    @staticmethod
    def _utf16_units(s):
        encoded = s.encode('utf-16-be')
        return [(encoded[i] << 8) | encoded[i + 1] for i in range(0, len(encoded), 2)]

    def matchInPattern(self, ch):
        for i in range(self.patLen - 1, -1, -1):
            if self.pattern_units[i] == ch:
                return i
        return -1

    def mismatchInText(self, currentPos):
        for i in range(self.patLen - 1, -1, -1):
            if self.pattern_units[i] != self.text_units[currentPos + i]:
                return currentPos + i
        return -1

    def badCharacterHeuristic(self):
        positions = []
        i = 0

        bad_char_heuristic = {}
        for j in range(self.patLen):
            bad_char_heuristic[self.pattern_units[j]] = j

        if self.patLen == 0:
            for j in range(self.textLen + 1):
                positions.append(j)
            return positions

        while i <= self.textLen - self.patLen:
            mismatch_index = self.mismatchInText(i)
            if mismatch_index == -1:
                positions.append(i)
                i += self.patLen
            else:
                mismatch_char = self.text_units[mismatch_index]
                match_index = bad_char_heuristic.get(mismatch_char, -1)
                if match_index >= 0:
                    i += max(1, mismatch_index - i - match_index)
                else:
                    i += mismatch_index - i + 1

        return positions