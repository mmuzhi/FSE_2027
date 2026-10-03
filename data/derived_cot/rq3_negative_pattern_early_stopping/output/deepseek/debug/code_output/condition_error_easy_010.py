class Solution:
    def convertToTitle(self, n: int) -> str:
        ans = ""
        while n > 0:
            n -= 1
            ans += chr(ord('A') + n % 26)
            n //= 26
        return ans[::-1]