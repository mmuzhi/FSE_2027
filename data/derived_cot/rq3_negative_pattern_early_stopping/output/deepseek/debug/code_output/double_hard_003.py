from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10 ** 9 + 7
        n = len(s)
        mem = defaultdict(int)

        def dfs(i: int, val: int) -> int:
            if i == n + 1:
                return 1
            key = (i, val)
            if key in mem:
                return mem[key]
            total = 0
            if s[i - 1] == 'D':
                for nxt in range(val):
                    total = (total + dfs(i + 1, nxt)) % MOD
            else:
                for nxt in range(val + 1, i + 1):
                    total = (total + dfs(i + 1, nxt)) % MOD
            mem[key] = total
            return total

        return dfs(1, 0)