class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        before = 0
        after = len(s) - 1
        l = list(s)
        while before < after:
            if l[before] != l[after]:
                l[before] = l[after] = min(l[before], l[after])
            before += 1
            after -= 1
        return "".join(l)