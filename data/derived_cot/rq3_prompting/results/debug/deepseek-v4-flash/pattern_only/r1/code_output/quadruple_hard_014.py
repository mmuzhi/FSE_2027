class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        mem = {}

        def dfs(i: int, val: int = 0) -> int:
            if i == len(s):
                return 1
            if (i, val) in mem:
                return mem[i, val]

            total = 0
            if s[i] == 'D':
                for nxt in range(val + 1):
                    total = (total + dfs(i + 1, nxt)) % MOD
            else:
                for nxt in range(val + 1, i + 2):
                    total = (total + dfs(i + 1, nxt)) % MOD

            mem[i, val] = total
            return total

        return dfs(0, 0)