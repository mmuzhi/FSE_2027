class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        def isForbidden(s):
            for f in forbidden:
                if f in s:
                    return True
            return False
        
        n = len(word)
        res = 0
        i = 0
        for j in range(n):
            while i <= j and isForbidden(word[i:j+1]):
                i += 1
            res = max(res, j - i + 1)
        return res