class Solution:
    def alternateDigitSum(self, n: int) -> int:
        s = str(n)
        count = 0
        for i, ch in enumerate(s):
            digit = int(ch)
            if i % 2 == 0:
                count += digit
            else:
                count -= digit
        return count