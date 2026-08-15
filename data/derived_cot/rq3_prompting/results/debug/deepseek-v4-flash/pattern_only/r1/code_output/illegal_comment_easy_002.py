class Solution:
    def alternateDigitSum(self, n: int) -> int:
        s = str(n)
        count = 0
        for i, ch in enumerate(s):
            if i % 2 == 0:
                count += int(ch)
            else:
                count -= int(ch)
        return count