class Solution:
    def alternateDigitSum(self, n: int) -> int:
        s = str(n)
        total = 0
        for i, ch in enumerate(s):
            if i % 2 == 0:
                total += int(ch)
            else:
                total -= int(ch)
        return total