class Solution:
    def longestWPI(self, A):
        n = len(A)
        prefix = 0
        min_prefix = 0
        min_index = 0
        ans = 0
        for i in range(n):
            step = 1 if A[i] > 8 else -1
            prefix += step
            if prefix < min_prefix:
                min_prefix = prefix
                min_index = i+1
            elif prefix > min_prefix:
                ans = max(ans, i - min_index + 2)
        return ans
