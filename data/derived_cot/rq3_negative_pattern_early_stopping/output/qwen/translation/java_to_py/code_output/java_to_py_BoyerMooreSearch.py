class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.textLen = len(text)
        self.patLen = len(pattern)
    
    def match_in_pattern(self, ch):
        for idx in range(self.patLen-1, -1, -1):
            if self.pattern[idx] == ch:
                return idx
        return -1

    def mismatch_in_text(self, current_pos):
        for j in range(self.patLen-1, -1, -1):
            if self.text[current_pos + j] != self.pattern[j]:
                return current_pos + j
        return -1

    def bad_character_heuristic(self):
        if self.patLen == 0:
            return list(range(0, self.textLen + 1))
        
        bad_char_heuristic = {}
        for idx, char in enumerate(self.pattern):
            bad_char_heuristic[char] = idx
        
        positions = []
        i = 0
        
        while i <= self.textLen - self.patLen:
            mismatch_index = self.mismatch_in_text(i)
            if mismatch_index == -1:
                positions.append(i)
                i += self.patLen
            else:
                char_at_mismatch = self.text[mismatch_index]
                match_index = bad_char_heuristic.get(char_at_mismatch, -1)
                if match_index >= 0:
                    shift = max(1, mismatch_index - i - match_index)
                    i += shift
                else:
                    i += mismatch_index - i + 1
        
        return positions