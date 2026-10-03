from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        r, c = len(pizza), len(pizza[0])
        pref = [[0]*c for _ in range(r)]
        total = 0
        for i in range(r):
            for j in range(c):
                if pizza[i][j] == 'A':
                    total += 1
                top = pref[i-1][j] if i>0 else 0
                left = pref[i][j-1] if j>0 else 0
                top_left = pref[i-1][j-1] if i>0 and j>0 else 0
                pref[i][j] = top + left - top_left + (1 if pizza[i][j]=='A' else 0)
        if total < k:
            return 0
        if k == 1:
            return 1

        def apples_in_rect(i1, j1, i2, j2):
            a = pref[i2][j2]
            if i1>0: a -= pref[i1-1][j2]
            if j1>0: a -= pref[i2][j1-1]
            if i1>0 and j1>0: a += pref[i1-1][j1-1]
            return a

        @lru_cache(None)
        def dfs(i, j, pieces):
            if pieces == 1:
                return 1 if apples_in_rect(i, j, r-1, c-1) > 0 else 0
            ans = 0
            for h in range(i, r-1):
                if apples_in_rect(i, j, h, c-1) > 0:
                    ans += dfs(h+1, j, pieces-1)
            for v in range(j, c-1):
                if apples_in_rect(i, j, r-1, v) > 0:
                    ans += dfs(i, v+1, pieces-1)
            return ans % MOD

        return dfs(0, 0, k) % MOD