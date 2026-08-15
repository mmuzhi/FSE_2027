from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1_000_000_007
        m, n = len(pizza), len(pizza[0])

        pref = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                pref[i + 1][j + 1] = (
                    pref[i][j + 1] + pref[i + 1][j] - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        if pref[m][n] < k:
            return 0

        def has_apple(r1, c1, r2, c2):
            return (
                pref[r2 + 1][c2 + 1]
                - pref[r1][c2 + 1]
                - pref[r2 + 1][c1]
                + pref[r1][c1]
            ) > 0

        @lru_cache(None)
        def dp(i, j, pieces):
            if pieces == 1:
                return 1 if has_apple(i, j, m - 1, n - 1) else 0

            ans = 0

            for r in range(i, m - 1):
                if has_apple(i, j, r, n - 1):
                    ans += dp(r + 1, j, pieces - 1)

            for c in range(j, n - 1):
                if has_apple(i, j, m - 1, c):
                    ans += dp(i, c + 1, pieces - 1)

            return ans % MOD

        return dp(0, 0, k) % MOD