from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10**9 + 7
        r, c = len(pizza), len(pizza[0])
        ps = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(r):
            for j in range(c):
                ps[i+1][j+1] = (ps[i+1][j] + ps[i][j+1] - ps[i][j] + 
                                (1 if pizza[i][j] == 'A' else 0))
        
        def has_apple(ri, rj, bi, bj):
            """return True if rectangle (ri,rj) to (bi,bj) has at least one apple"""
            return (ps[bi+1][bj+1] - ps[ri][bj+1] - 
                    ps[bi+1][rj] + ps[ri][rj]) > 0
        
        @lru_cache(None)
        def dp(i, j, cuts):
            """number of ways to cut sub-pizza (i,j) -> (r-1,c-1) into cuts+1 pieces"""
            if cuts == 0:
                return 1 if has_apple(i, j, r-1, c-1) else 0
            ans = 0
            for nr in range(i, r-1):
                if has_apple(i, j, nr, c-1):
                    ans += dp(nr+1, j, cuts-1)
            for nc in range(j, c-1):
                if has_apple(i, j, r-1, nc):
                    ans += dp(i, nc+1, cuts-1)
            return ans % MOD
        
        return dp(0, 0, k-1) % MOD