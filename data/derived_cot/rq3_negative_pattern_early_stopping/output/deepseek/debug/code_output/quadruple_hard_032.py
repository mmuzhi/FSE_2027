from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        mem = defaultdict(int)
        
        def dfs(i: int, last: int = 0) -> int:
            if i == len(s):
                return 1
            key = (i, last)
            if key in mem:
                return mem[key]
            total = 0
            if s[i] == 'D':
                for nxt in range(last):
                    total += dfs(i + 1, nxt)
                    total %= MOD
            else:  # 'I'
                for nxt in range(last + 1, len(s) + 1):
                    total += dfs(i + 1, nxt)
                    total %= MOD
            mem[key] = total
            return total
        
        ans = 0
        for first in range(len(s) + 1):
            ans += dfs(1, first)
            ans %= MOD
        return ans