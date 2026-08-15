from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        R, C = len(pizza), len(pizza[0])

        pref = [[0] * (C + 1) for _ in range(R + 1)]
        for i in range(R):
            for j in range(C):
                pref[i + 1][j + 1] = (
                    pref[i][j + 1] + pref[i + 1][j] - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        def has_apple(r1: int, c1: int, r2: int, c2: int) -> bool:
            return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1] > 0

        @lru_cache(None)
        def dp(r: int, c: int, pieces: int) -> int:
            if not has_apple(r, c, R - 1, C - 1):
                return 0
            if pieces == 1:
                return 1

            ans = 0

            for nr in range(r, R - 1):
                if has_apple(r, c, nr, C - 1):
                    ans += dp(nr + 1, c, pieces - 1)

            for nc in range(c, C - 1):
                if has_apple(r, c, R - 1, nc):
                    ans += dp(r, nc + 1, pieces - 1)

            return ans % MOD

        if pref[R][C] < k:
            return 0

        return dp(0, 0, k)