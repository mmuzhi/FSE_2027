class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_len = len(text)
        self.pat_len = len(pattern)

    def match_in_pattern(self, c):
        for i in range(self.pat_len - 1, -1, -1):
            if c == self.pattern[i]:
                return i
        return -1

    def mismatch_in_text(self, currentPos):
        for i in range(self.pat_len - 1, -1, -1):
            if self.pattern[i] != self.text[currentPos + i]:
                return currentPos + i
        return -1

    def bad_character_heuristic(self):
        positions = []
        i = 0
        while i <= self.text_len - self.pat_len:
            mismatch_index = self.mismatch_in_text(i)
            if mismatch_index == -1:
                positions.append(i)
                i += 1
            else:
                mismatched_char = self.text[mismatch_index]
                match_index = self.match_in_pattern(mismatched_char)
                if match_index == -1:
                    i += (mismatch_index - i + 1)
                else:
                    i += (mismatch_index - match_index)
        return positions