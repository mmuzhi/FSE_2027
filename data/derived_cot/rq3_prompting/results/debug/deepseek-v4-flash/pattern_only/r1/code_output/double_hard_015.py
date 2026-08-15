from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10**9 + 7
        r = len(pizza)
        c = len(pizza[0])

        pref = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(r):
            for j in range(c):
                pref[i + 1][j + 1] = (
                    pref[i][j + 1]
                    + pref[i + 1][j]
                    - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        if pref[r][c] < k:
            return 0

        def has_apple(top: int, left: int, bottom: int, right: int) -> bool:
            return (
                pref[bottom + 1][right + 1]
                - pref[top][right + 1]
                - pref[bottom + 1][left]
                + pref[top][left]
            ) > 0

        @lru_cache(None)
        def dp(top: int, left: int, pieces: int) -> int:
            if pieces == 1:
                return 1 if has_apple(top, left, r - 1, c - 1) else 0

            ans = 0

            for cut in range(top, r - 1):
                if has_apple(top, left, cut, c - 1):
                    ans = (ans + dp(cut + 1, left, pieces - 1)) % MOD

            for cut in range(left, c - 1):
                if has_apple(top, left, r - 1, cut):
                    ans = (ans + dp(top, cut + 1, pieces - 1)) % MOD

            return ans

        return dp(0, 0, k)