class Solution:
    def alternateDigitSum(self, n: int) -> int:
        s = str(n)
        count = 0
        for i in range(len(s)):
            if i % 2 == 0:
                count += int(s[i])
            else:
                count -= int(s[i])
        return count