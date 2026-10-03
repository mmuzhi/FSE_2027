class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        s1 = ''.join(char for char in s1 if char in set(s2))
        
        ptr = 0
        count = 0
        total_occurrences = 0
        
        for _ in range(n1):
            for char in s2:
                while ptr < len(s1) and s1[ptr] != char:
                    ptr += 1
                    count += 1
                if ptr < len(s1):
                    ptr += 1
                    count += 1
                else:
                    break
            else:
                total_occurrences += 1
                if total_occurrences >= n2:
                    return n2
            if ptr >= len(s1):
                break
        
        return total_occurrences // n2
