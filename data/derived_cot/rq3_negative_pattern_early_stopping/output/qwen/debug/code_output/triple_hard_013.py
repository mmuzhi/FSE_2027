class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        len_s1 = len(s1)
        len_s2 = len(s2)
        
        # Build the prefix function (failure function) for s2.
        pi = [0] * len_s2
        j = 0
        for i in range(1, len_s2):
            while j > 0 and s2[i] != s2[j]:
                j = pi[j-1]
            if s2[i] == s2[j]:
                j += 1
            pi[i] = j
        
        total_occurrences = 0
        j = 0
        
        for i in range(n1 * len_s1):
            char = s1[i % len_s1]
            while j > 0 and char != s2[j]:
                j = pi[j-1]
            if char == s2[j]:
                j += 1
            else:
                j = 0
            if j == len_s2:
                total_occurrences += 1
                j = pi[j-1]
        
        return total_occurrences // n2