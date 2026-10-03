from typing import List
from functools import cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        self.ps = [[0] * (self.c + 1) for _ in range(self.r + 1)]
        for i in range(self.r):
            for j in range(self.c):
                self.ps[i+1][j+1] = self.ps[i][j+1] + self.ps[i+1][j] - self.ps[i][j] + (1 if pizza[i][j] == 'A' else 0)
        
        if self.ps[self.r][self.c] < k:
            return 0
        
        return self.getWays(0, 0, k) % (1000000007)
    
    def has_apple(self, r1, c1, r2, c2):
        return self.ps[r2+1][c2+1] - self.ps[r1][c2+1] - self.ps[r2+1][c1] + self.ps[r1][c1] > 0

    @cache
    def getWays(self, i, j, k):
        if k == 1:
            return 1 if self.has_apple(i, j, self.r - 1, self.c - 1) else 0
        
        t_cnt = 0
        for nr in range(i, self.r - 1):
            if self.has_apple(i, j, nr, self.c - 1):
                t_cnt += self.getWays(nr + 1, j, k - 1)
                
        for nc in range(j, self.c - 1):
            if self.has_apple(i, j, self.r - 1, nc):
                t_cnt += self.getWays(i, nc + 1, k - 1)
                
        return t_cnt % 1000000007