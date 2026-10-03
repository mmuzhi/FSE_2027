from typing import List
from functools import cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10**9 + 7
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        self.pref = [[0] * (self.c + 1) for _ in range(self.r + 1)]
        total_apples = 0
        for i in range(self.r):
            row_sum = 0
            for j in range(self.c):
                apple = 1 if pizza[i][j] == 'A' else 0
                row_sum += apple
                self.pref[i+1][j+1] = self.pref[i][j+1] + row_sum
                total_apples += apple
        
        if total_apples < k:
            return 0
        if k == 1:
            return 1
        
        @cache
        def dfs(i: int, j: int, k: int) -> int:
            if k == 1:
                apples = (self.pref[self.r][self.c] - self.pref[i][self.c] -
                          self.pref[self.r][j] + self.pref[i][j])
                return 1 if apples > 0 else 0
            
            total = 0
            for h in range(i, self.r - 1):
                top_apples = (self.pref[h+1][self.c] - self.pref[i][self.c] -
                              self.pref[h+1][j] + self.pref[i][j])
                if top_apples > 0:
                    total = (total + dfs(h + 1, j, k - 1)) % MOD
            for v in range(j, self.c - 1):
                left_apples = (self.pref[self.r][v+1] - self.pref[i][v+1] -
                               self.pref[self.r][j] + self.pref[i][j])
                if left_apples > 0:
                    total = (total + dfs(i, v + 1, k - 1)) % MOD
            return total % MOD
        
        return dfs(0, 0, k)