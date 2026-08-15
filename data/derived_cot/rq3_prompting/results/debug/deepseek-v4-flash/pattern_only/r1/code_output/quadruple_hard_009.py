from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        R, C = len(pizza), len(pizza[0])
        MOD = 1000000007

        pref = [[0] * (C + 1) for _ in range(R + 1)]
        for i in range(R):
            row_sum = 0
            for j in range(C):
                if pizza[i][j] == 'A':
                    row_sum += 1
                pref[i + 1][j + 1] = pref[i][j + 1] + row_sum

        def count_apples(r1, c1, r2, c2):
            return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1]

        if count_apples(0, 0, R - 1, C - 1) < k:
            return 0

        @lru_cache(None)
        def dp(r, c, cuts_left):
            if count_apples(r, c, R - 1, C - 1) < cuts_left:
                return 0
            if cuts_left == 1:
                return 1

            ans = 0
            for i in range(r, R - 1):
                if count_apples(r, c, i, C - 1) > 0:
                    ans = (ans + dp(i + 1, c, cuts_left - 1)) % MOD

            for j in range(c, C - 1):
                if count_apples(r, c, R - 1, j) > 0:
                    ans = (ans + dp(r, j + 1, cuts_left - 1)) % MOD

            return ans

        return dp(0, 0, k) % MOD