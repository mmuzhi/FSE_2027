class Solution:
    def minCost(self, A, K):
        n = len(A)
        dp = [0] + [float('inf')] * n
        for i in range(n):
            cnt = {}
            val = K
            for j in range(i, -1, -1):
                x = A[j]
                c = cnt.get(x, 0)
                if c == 1:
                    val += 2
                elif c >= 2:
                    val += 1
                cnt[x] = c + 1
                dp[i + 1] = min(dp[i + 1], dp[j] + val)
        return dp[-1]