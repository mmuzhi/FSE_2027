class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        dp = [1]

        for ch in s:
            L = len(dp)
            ndp = [0] * (L + 1)

            if ch == 'I':
                pref = 0
                for v in range(L + 1):
                    ndp[v] = pref
                    if v < L:
                        pref = (pref + dp[v]) % MOD
            else:
                suff = 0
                for v in range(L, -1, -1):
                    if v < L:
                        suff = (suff + dp[v]) % MOD
                    ndp[v] = suff

            dp = ndp

        return sum(dp) % MOD