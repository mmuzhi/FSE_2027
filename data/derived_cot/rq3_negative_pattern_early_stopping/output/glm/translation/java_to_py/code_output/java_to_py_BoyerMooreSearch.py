class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.textLen = len(text)
        self.patLen = len(pattern)

    def matchInPattern(self, ch):
        return self.pattern.rfind(ch)

    def mismatchInText(self, currentPos):
        for i in range(self.patLen - 1, -1, -1):
            if self.pattern[i] != self.text[currentPos + i]:
                return currentPos + i
        return -1

    def badCharacterHeuristic(self):
        positions = []
        i = 0

        badCharHeuristic = {}
        for j in range(self.patLen):
            badCharHeuristic[self.pattern[j]] = j

        if self.patLen == 0:
            for j in range(self.textLen + 1):
                positions.append(j)
            return positions

        while i <= self.textLen - self.patLen:
            mismatchIndex = self.mismatchInText(i)
            if mismatchIndex == -1:
                positions.append(i)
                i += self.patLen
            else:
                mismatchChar = self.text[mismatchIndex]
                matchIndex = badCharHeuristic.get(mismatchChar, -1)
                if matchIndex >= 0:
                    i += max(1, mismatchIndex - i - matchIndex)
                else:
                    i += mismatchIndex - i + 1

        return positions