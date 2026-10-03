class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not s2:
            return 0
        
        if not set(s2).issubset(set(s1)):
            return 0
        
        pos_map = {}
        for char in s2:
            pos_map[char] = [index for index, c in enumerate(s1) if c == char]
        
        i = 0
        j = 0
        total = 0
        seen = {}
        
        while j < n1 * len(s1) and i < len(s2):
            char = s2[i]
            if char not in pos_map:
                return 0
            
            current_rep = j // len(s1)
            current_index = j % len(s1)
            next_occurrence_in_current_rep = None
