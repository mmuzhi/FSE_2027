from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mod = 10**9 + 7
        n = len(s)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for j in range(n + 1):
            dp[0][j] = 1  # first position: any of the numbers 0..n can be chosen
        
        for i in range(1, n + 1):
            if s[i - 1] == 'D':
                prefix_sum = 0
                for j in range(n - i, -1, -1):
                    prefix_sum = (prefix_sum + dp[i - 1][j + 1]) % mod
                    dp[i][j] = prefix_sum
            else:
                prefix_sum = 0
                for j in range(n - i + 1):
                    prefix_sum = (prefix_sum + dp[i - 1][j]) % mod
                    dp[i][j] = prefix_sum
        
        return dp[n][0] % mod