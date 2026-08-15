from typing import List
from functools import lru_cache

MOD = 10**9 + 7

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        r = len(pizza)
        c = len(pizza[0])

        pref = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(r):
            for j in range(c):
                pref[i + 1][j + 1] = (
                    pref[i][j + 1] + pref[i + 1][j] - pref[i][j]
                    + (1 if pizza[i][j] == 'A' else 0)
                )

        def has_apple(top: int, left: int, bottom: int, right: int) -> bool:
            return (
                pref[bottom + 1][right + 1]
                - pref[top][right + 1]
                - pref[bottom + 1][left]
                + pref[top][left]
            ) > 0

        @lru_cache(maxsize=None)
        def dp(i: int, j: int, pieces: int) -> int:
            if pieces == 1:
                return 1 if has_apple(i, j, r - 1, c - 1) else 0

            ans = 0
            for row in range(i, r - 1):
                if has_apple(i, j, row, c - 1):
                    ans += dp(row + 1, j, pieces - 1)

            for col in range(j, c - 1):
                if has_apple(i, j, r - 1, col):
                    ans += dp(i, col + 1, pieces - 1)

            return ans % MOD

        if pref[r][c] < k:
            return 0

        return dp(0, 0, k) % MOD