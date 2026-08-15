from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10**9 + 7
        rows = len(pizza)
        cols = len(pizza[0])

        pref = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(rows):
            for j in range(cols):
                pref[i + 1][j + 1] = (
                    pref[i][j + 1] + pref[i + 1][j] - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        def has_apple(r1, c1, r2, c2):
            return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1] > 0

        if pref[rows][cols] < k:
            return 0

        @lru_cache(None)
        def dp(i, j, pieces):
            if pieces == 1:
                return 1 if has_apple(i, j, rows - 1, cols - 1) else 0

            ans = 0
            for r in range(i, rows - 1):
                if has_apple(i, j, r, cols - 1):
                    ans += dp(r + 1, j, pieces - 1)
                    ans %= MOD

            for c in range(j, cols - 1):
                if has_apple(i, j, rows - 1, c):
                    ans += dp(i, c + 1, pieces - 1)
                    ans %= MOD

            return ans

        return dp(0, 0, k) % MOD