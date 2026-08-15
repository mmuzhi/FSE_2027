class Solution:
    def alternateDigitSum(self, n: int) -> int:
        count = 0
        s = str(n)
        for i in range(len(s)):
            if i % 2 == 0:
                count += int(s[i])
            else:
                count -= int(s[i])
        return count