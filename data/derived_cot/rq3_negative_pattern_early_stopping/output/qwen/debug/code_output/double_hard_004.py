from functools import cache

class Solution:
    mod = 1000000007

    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        self.pref = [[0] * (self.c + 1) for _ in range(self.r + 1)]
        for i in range(self.r):
            for j in range(self.c):
                self.pref[i+1][j+1] = self.pref[i][j+1] + self.pref[i+1][j] - self.pref[i][j] + (1 if pizza[i][j] == 'A' else 0)
                
        tot_apples = self.pref[self.r][self.c]
        if tot_apples < k:
            return 0
            
        if k == 1:
            if self.pref[self.r][self.c] - self.pref[0][0] > 0:
                return 1
            else:
                return 0
        
        @cache
        def getWays(i, j, k):
            if k == 1:
                apples = self.pref[self.r][self.c] - self.pref[i][self.c] - self.pref[self.r][j] + self.pref[i][j]
                if apples > 0:
                    return 1
                else:
                    return 0
                    
            total = 0
            for r in range(i+1, self.r-1):
                if self.pref[r+1][self.c] - self.pref[i][self.c] - self.pref[r+1][j] + self.pref[i][j] > 0:
                    total = (total + getWays(r+1, j, k-1)) % self.mod
                    
            for c in range(j+1, self.c-1):
                if self.pref[self.r][c+1] - self.pref[i][c+1] - self.pref[self.r][j] + self.pref[i][j] > 0:
                    total = (total + getWays(i, c+1, k-1)) % self.mod
                    
            return total
            
        return getWays(0, 0, k) % self.mod