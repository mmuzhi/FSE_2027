class Solution:
    def alternateDigitSum(self, n: int) -> int:
        result = str(n)
        total = 0
        for i in range(len(result)):
            if i % 2 == 0:
                total = total + int(result[i])
            else:
                total = total - int(result[i])
        return total