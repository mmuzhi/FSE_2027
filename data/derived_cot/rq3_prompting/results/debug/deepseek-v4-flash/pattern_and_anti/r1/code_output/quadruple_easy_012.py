class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        before = 0
        after = len(s) - 1
        chars = list(s)

        while before < after:
            if chars[before] != chars[after]:
                smallest = min(chars[before], chars[after])
                chars[before] = smallest
                chars[after] = smallest
            before += 1
            after -= 1

        return "".join(chars)