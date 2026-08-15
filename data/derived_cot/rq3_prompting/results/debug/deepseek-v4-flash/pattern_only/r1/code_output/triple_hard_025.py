class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s)
        MOD = 10**9 + 7
        memo = {}

        def dfs(i, val):
            if i == n:
                return 1
            key = (i, val)
            if key in memo:
                return memo[key]

            total = 0
            if s[i] == 'D':
                for nxt in range(val):
                    total += dfs(i + 1, nxt)
            else:
                for nxt in range(val, n - i):
                    total += dfs(i + 1, nxt)

            total %= MOD
            memo[key] = total
            return total

        return sum(dfs(0, val) for val in range(n + 1)) % MOD