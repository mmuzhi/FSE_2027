class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        memo = {}

        def dfs(i, val):
            if i == len(s):
                return 1
            if (i, val) in memo:
                return memo[(i, val)]

            total = 0
            if s[i] == 'D':
                for nxt in range(val + 1):
                    total = (total + dfs(i + 1, nxt)) % MOD
            else:
                for nxt in range(val + 1, i + 2):
                    total = (total + dfs(i + 1, nxt)) % MOD

            memo[(i, val)] = total
            return total

        return dfs(0, 0)