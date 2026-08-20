class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        j = 0
        num = -1
        for i in range(1, n + 1):
            if n % i == 0:
                num = i
                j += 1
            if j == k:
                break
        return num if j == k else -1