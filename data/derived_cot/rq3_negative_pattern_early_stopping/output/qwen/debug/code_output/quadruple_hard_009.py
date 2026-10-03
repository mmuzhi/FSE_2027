from functools import cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        n = len(pizza)
        m = len(pizza[0])
        pref = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(m):
                pref[i+1][j+1] = pref[i][j+1] + pref[i+1][j] - pref[i][j] + (1 if pizza[i][j] == 'A' else 0)
        
        total_apples = pref[n][m]
        if total_apples < k:
            return 0
        
        @cache
        def getWays(r, c, k):
            if k == 1:
                apples_here = pref[n][m] - pref[r][m] - pref[n][c] + pref[r][c]
                return 1 if apples_here > 0 else 0
            
            total = 0
            for i in range(r + 1, n):
                top_apples = pref[i][m] - pref[r][m] - pref[i][c] + pref[r][c]
                if top_apples > 0:
                    total = (total + getWays(i, c, k - 1)) % MOD
            
            for j in range(c + 1, m):
                left_apples = pref[n][j] - pref[r][j] - pref[n][c] + pref[r][c]
                if left_apples > 0:
                    total = (total + getWays(r, j, k - 1)) % MOD
            
            return total % MOD
        
        return getWays(0, 0, k) % MOD