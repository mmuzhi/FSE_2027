from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        mem = defaultdict(int)
        n = len(s)

        def dfs(i, val):
            if i == n:
                return 1
            key = (i, val)
            if key in mem:
                return mem[key]
            total = 0
            if s[i] == 'D':
                for ind in range(0, val):
                    total += dfs(i + 1, ind)
            else:  # 'I'
                for ind in range(val + 1, i + 2):
                    total += dfs(i + 1, ind)
            total %= MOD
            mem[key] = total
            return total

        ans = 0
        for first in range(n + 1):
            ans = (ans + dfs(0, first)) % MOD
        return ans