from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        r = len(pizza)
        c = len(pizza[0])
        pref = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(r):
            for j in range(c):
                pref[i+1][j+1] = pref[i][j+1] + pref[i+1][j] - pref[i][j] + (1 if pizza[i][j] == 'A' else 0)

        def hasApple(i, j):
            return pref[r][c] - pref[i][c] - pref[r][j] + pref[i][j] > 0

        @lru_cache(None)
        def dp(i, j, k):
            if k == 1:
                return 1 if hasApple(i, j) else 0
            ans = 0
            for p in range(i, r - 1):
                top_apples = pref[p+1][c] - pref[i][c] - pref[p+1][j] + pref[i][j]
                if top_apples > 0:
                    ans = (ans + dp(p+1, j, k-1)) % MOD
            for q in range(j, c - 1):
                left_apples = pref[r][q+1] - pref[i][q+1] - pref[r][j] + pref[i][j]
                if left_apples > 0:
                    ans = (ans + dp(i, q+1, k-1)) % MOD
            return ans % MOD

        total_apples = pref[r][c]
        if total_apples < k:
            return 0
        return dp(0, 0, k) % MOD