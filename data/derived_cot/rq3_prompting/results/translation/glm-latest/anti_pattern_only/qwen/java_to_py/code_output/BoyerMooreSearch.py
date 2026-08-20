class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_len = len(text)
        self.pat_len = len(pattern)

    def match_in_pattern(self, ch):
        return self.pattern.rfind(ch)

    def mismatch_in_text(self, current_pos):
        for i in range(self.pat_len - 1, -1, -1):
            if self.pattern[i] != self.text[current_pos + i]:
                return current_pos + i
        return -1

    def bad_character_heuristic(self):
        positions = []
        i = 0

        bad_char_heuristic = {}
        for j in range(self.pat_len):
            bad_char_heuristic[self.pattern[j]] = j

        if self.pat_len == 0:
            for j in range(self.text_len + 1):
                positions.append(j)
            return positions

        while i <= self.text_len - self.pat_len:
            mismatch_index = self.mismatch_in_text(i)
            if mismatch_index == -1:
                positions.append(i)
                i += self.pat_len
            else:
                mismatch_char = self.text[mismatch_index]
                match_index = bad_char_heuristic.get(mismatch_char, -1)
                if match_index >= 0:
                    i += max(1, mismatch_index - i - match_index)
                else:
                    i += mismatch_index - i + 1
        return positions