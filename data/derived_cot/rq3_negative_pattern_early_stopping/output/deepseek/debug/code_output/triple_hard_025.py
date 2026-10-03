class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for j in range(n + 1):
            dp[0][j] = 1
        for i in range(1, n + 1):
            if s[i - 1] == 'I':
                for j in range(n - i + 1):
                    dp[i][j] = (dp[i][j - 1] + dp[i - 1][j - 1]) % MOD
            else:
                for j in range(n - i, -1, -1):
                    dp[i][j] = (dp[i][j + 1] + dp[i - 1][j]) % MOD
        return dp[n][0]