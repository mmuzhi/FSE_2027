class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        l = list(s)
        n = len(l)
        for i in range(n // 2):
            if l[i] > l[n-1-i]:
                l[i], l[n-1-i] = l[n-1-i], l[i]
        return "".join(l)
