class Solution:
    def convertToTitle(self, n: int) -> str:
        s = ""
        while n > 0:
            n, r = divmod(n-1, 26)
            s = chr(65 + r) + s
        return s