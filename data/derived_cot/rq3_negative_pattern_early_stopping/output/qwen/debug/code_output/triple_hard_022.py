class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not s2:
            return 0
        
        # Filter s1 to keep only characters in s2
        s1_filtered = ''.join(char for char in s1 if char in set(s2))
        if not s1_filtered:
            return 0
        
        L = len(s1_filtered)
        total_length = n1 * L
        
        # If s2 is longer than the big string, return 0
        if len(s2) > total_length:
            return 0
        
        # Precompute the positions of each character in s1_filtered
        char_positions = {}
        for char in set(s2):
            char_positions[char] = [i for i, c in enumerate(s1_filtered) if c == char]
        
        # If any character in s2 is not in s1_filtered, then we cannot form any s2
        for char in s2:
            if char not in char_positions:
                return 0
        
        #
