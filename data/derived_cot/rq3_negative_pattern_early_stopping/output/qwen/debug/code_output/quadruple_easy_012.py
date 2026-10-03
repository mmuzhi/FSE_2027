class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        s_list = list(s)
        left, right = 0, len(s_list) - 1
        while left < right:
            if s_list[left] > s_list[right]:
                s_list[left] = s_list[right]
            else:
                s_list[right] = s_list[left]
            left += 1
            right -= 1
        return "".join(s_list)