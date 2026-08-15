class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        dp = [1]

        for i in range(1, n + 1):
            prefix = [0] * (i + 1)
            for k in range(i):
                prefix[k + 1] = (prefix[k] + dp[k]) % MOD

            ndp = [0] * (i + 1)
            if s[i - 1] == 'I':
                for j in range(i + 1):
                    ndp[j] = prefix[j]
            else:
                for j in range(i + 1):
                    ndp[j] = (prefix[i] - prefix[j]) % MOD

            dp = ndp

        return sum(dp) % MOD