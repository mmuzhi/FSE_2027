class Solution:
    def alternateDigitSum(self, n: int) -> int:
        count = 0
        n_str = str(n)
        for i in range(len(n_str)):
            if i % 2 == 0:
                count += int(n_str[i])
            else:
                count -= int(n_str[i])
        return count