class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_len = len(text)
        self.pat_len = len(pattern)

    def match_in_pattern(self, c):
        # Search from the end of the pattern backwards for the character c.
        for i in range(self.pat_len - 1, -1, -1):
            if self.pattern[i] == c:
                return i
        return -1

    def mismatch_in_text(self, currentPos):
        # Check from the current position in the text, comparing with the pattern.
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
                # No mismatch, so we found a match at position i.
                positions.append(i)
                i += 1
            else:
                mismatched_char = self.text[mismatch_index]
                match_index = self.match_in_pattern(mismatched_char)
                if match_index == -1:
                    # The mismatched character does not occur in the pattern at all.
                    # We jump from mismatch_index to the next position after the current i.
                    i += (mismatch_index - i + 1)
                else:
                    # We jump from mismatch_index to the position right after the occurrence of the same character in the pattern.
                    i += (mismatch_index - match_index)
        return positions