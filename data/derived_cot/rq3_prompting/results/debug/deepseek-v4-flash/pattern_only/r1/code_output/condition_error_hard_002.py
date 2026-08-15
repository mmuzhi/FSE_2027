class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        mem = {}

        def dfs(i, val):
            if i == n:
                return 1
            key = (i, val)
            if key in mem:
                return mem[key]

            total = 0
            if s[i] == 'D':
                for nxt in range(val + 1):
                    total = (total + dfs(i + 1, nxt)) % MOD
            else:
                for nxt in range(val + 1, i + 2):
                    total = (total + dfs(i + 1, nxt)) % MOD

            mem[key] = total
            return total

        return dfs(0, 0)