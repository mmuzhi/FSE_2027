from functools import lru_cache

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        
        @lru_cache(None)
        def dp(i: int, prev: int) -> int:
            if i == n:
                return 1
            total = 0
            if s[i] == 'D':
                for nxt in range(prev):
                    total = (total + dp(i + 1, nxt)) % MOD
            else:  # 'I'
                for nxt in range(prev + 1, i + 2):
                    total = (total + dp(i + 1, nxt)) % MOD
            return total
        
        ans = 0
        for first in range(n + 1):
            ans = (ans + dp(1, first)) % MOD
        return ans