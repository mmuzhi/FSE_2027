class Solution:
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
        n = len(s)
        for i in range(0, n - k + 1):
            char = s[i]
            all_same = True
            for j in range(i, i + k):
                if s[j] != char:
                    all_same = False
                    break
            if not all_same:
                continue
            if i > 0 and s[i-1] == char:
                continue
            if i + k < n and s[i+k] == char:
                continue
            return True
        return False