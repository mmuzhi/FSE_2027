from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        rows, cols = len(pizza), len(pizza[0])
        MOD = 10**9 + 7

        pref = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            row_apples = 0
            for c in range(cols):
                if pizza[r][c] == 'A':
                    row_apples += 1
                pref[r + 1][c + 1] = pref[r][c + 1] + row_apples

        def has_apple(r1, c1, r2, c2):
            return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1] > 0

        @lru_cache(None)
        def dp(r, c, pieces):
            if not has_apple(r, c, rows - 1, cols - 1):
                return 0
            if pieces == 1:
                return 1

            ans = 0
            for cut_r in range(r, rows - 1):
                if has_apple(r, c, cut_r, cols - 1):
                    ans += dp(cut_r + 1, c, pieces - 1)

            for cut_c in range(c, cols - 1):
                if has_apple(r, c, rows - 1, cut_c):
                    ans += dp(r, cut_c + 1, pieces - 1)

            return ans % MOD

        if pref[rows][cols] < k:
            return 0

        return dp(0, 0, k)