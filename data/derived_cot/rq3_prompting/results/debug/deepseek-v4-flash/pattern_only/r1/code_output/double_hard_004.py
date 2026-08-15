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
                pref[i + 1][j + 1] = (
                    pref[i][j + 1] + pref[i + 1][j] - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        def has_apple(r1: int, c1: int, r2: int, c2: int) -> bool:
            return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1] > 0

        @lru_cache(None)
        def dp(i: int, j: int, pieces: int) -> int:
            if pieces == 1:
                return 1 if has_apple(i, j, r - 1, c - 1) else 0

            ans = 0
            for nr in range(i, r - 1):
                if has_apple(i, j, nr, c - 1):
                    ans = (ans + dp(nr + 1, j, pieces - 1)) % MOD

            for nc in range(j, c - 1):
                if has_apple(i, j, r - 1, nc):
                    ans = (ans + dp(i, nc + 1, pieces - 1)) % MOD

            return ans

        if sum(row.count('A') for row in pizza) < k:
            return 0

        return dp(0, 0, k) % MOD