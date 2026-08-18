from collections import defaultdict


class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mem = defaultdict(int)
        n = len(s)
        MOD = 10 ** 9 + 7

        def dfs(i, val=0):
            if i == n:
                return 1
            if (i, val) in mem:
                return mem[i, val]
            p = 0
            if s[i] == "D":
                for ind in range(0, val):
                    p += dfs(i + 1, ind)
            else:
                for ind in range(val, n - i):
                    p += dfs(i + 1, ind)
            p %= MOD
            mem[i, val] = p
            return p

        return sum(dfs(0, val) for val in range(n + 1)) % MOD