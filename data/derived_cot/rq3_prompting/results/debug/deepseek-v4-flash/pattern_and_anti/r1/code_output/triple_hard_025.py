class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        dp = [1] + [0] * n

        for i, ch in enumerate(s, 1):
            ndp = [0] * (i + 1)

            if ch == 'I':
                run = 0
                for j in range(i + 1):
                    ndp[j] = run
                    if j < i:
                        run = (run + dp[j]) % MOD
            else:
                run = 0
                for j in range(i, -1, -1):
                    ndp[j] = run
                    if j > 0:
                        run = (run + dp[j - 1]) % MOD

            dp = ndp

        return sum(dp) % MOD