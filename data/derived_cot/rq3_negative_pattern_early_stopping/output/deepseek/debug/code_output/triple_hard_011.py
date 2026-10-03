from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        self.pref = [[0] * (self.c + 1) for _ in range(self.r + 1)]
        tot_apples = 0
        for i in range(self.r):
            row_sum = 0
            for j in range(self.c):
                if pizza[i][j] == 'A':
                    row_sum += 1
                    tot_apples += 1
                self.pref[i+1][j+1] = self.pref[i][j+1] + row_sum
        
        if tot_apples < k:
            return 0
        if k == 1:
            return 1
        
        @lru_cache(None)
        def getWays(i: int, j: int, pieces: int) -> int:
            if pieces == 1:
                return 1 if self._has_apple(i, j, self.r-1, self.c-1) else 0
            
            total = 0
            for h in range(i, self.r - 1):
                if self._has_apple(i, j, h, self.c-1):
                    total += getWays(h+1, j, pieces-1)
            
            for v in range(j, self.c - 1):
                if self._has_apple(i, j, self.r-1, v):
                    total += getWays(i, v+1, pieces-1)
            
            return total % MOD
        
        return getWays(0, 0, k) % MOD
    
    def _has_apple(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        total = (self.pref[r2+1][c2+1] - self.pref[r1][c2+1] -
                 self.pref[r2+1][c1] + self.pref[r1][c1])
        return total > 0