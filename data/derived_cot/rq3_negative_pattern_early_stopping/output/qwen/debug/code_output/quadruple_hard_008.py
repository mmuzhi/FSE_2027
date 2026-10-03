class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        len_s1 = len(s1)
        len_s2 = len(s2)
        j = 0
        count = 0
        
        for i in range(n1 * len_s1):
            if s1[i % len_s1] == s2[j]:
                j = (j + 1) % len_s2
            if j == 0:
                count += 1
        
        return count // n2
