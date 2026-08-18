class Solution:
    def longestPrefix(self, s: str) -> str:
        n = len(s)
        lps = [0] * n
        j = 0
        for i in range(1, n):
            while j > 0 and s[i] != s[j]:
                j = lps[j - 1]

            if s[i] == s[j]:
                lps[i] = j + 1
                j += 1

        return s[:lps[-1]]