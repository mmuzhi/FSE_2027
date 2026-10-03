class Solution:
    def alternateDigitSum(self, n: int) -> int:
        s = str(abs(n))
        total = 0
        for i in range(len(s)):
            if i % 2 == 0:
                total += int(s[i])
            else:
                total -= int(s[i])
        return total