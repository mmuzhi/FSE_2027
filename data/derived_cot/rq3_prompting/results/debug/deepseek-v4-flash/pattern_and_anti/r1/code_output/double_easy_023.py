class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        chars = list(s)
        left, right = 0, len(s) - 1

        while left < right:
            if chars[left] != chars[right]:
                c = min(chars[left], chars[right])
                chars[left] = c
                chars[right] = c
            left += 1
            right -= 1

        return ''.join(chars)