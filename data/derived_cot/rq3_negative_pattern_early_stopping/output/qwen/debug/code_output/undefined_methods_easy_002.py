class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        before = 0
        after = len(s)-1
        l = [i for i in s]
        while before < after:
            # Use the built-in min function
            min_char = min(l[before], l[after])
            l[before] = min_char
            l[after] = min_char
            before += 1
            after -= 1
        return "".join(l)