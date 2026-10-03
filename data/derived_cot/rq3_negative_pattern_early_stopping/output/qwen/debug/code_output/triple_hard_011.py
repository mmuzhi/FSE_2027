from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        r = len(pizza)
        c = len(pizza[0])
        grid = [[1 if ch == 'A' else 0 for ch in row] for row in pizza]
        pref = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(1, r + 1):
            for j in range(1, c + 1):
                pref[i][j] = pref[i-1][j] + pref[i][j-1] - pref[i-1][j-1] + grid[i-1][j-1]
        
        total_apples = pref[r][c]
        if k > total_apples:
            return 0
        
        def has_apple(i, j, x, y):
            return pref[x+1][y+1] - pref[i][y+1] - pref[x+1][j] + pref[i][j] > 0
        
        @lru_cache(maxsize=None)
        def dp(i, j, k):
            if k == 1:
                return 1 if has_apple(i, j, r-1, c-1) else 0
            total_ways = 0
            for x in range(i+1, r):
                if has_apple(x, j, r-1, c-1):
                    total_ways = (total_ways + dp(i, x, k-1)) % 1000000007
            for y in range(j+1, c):
                if has_apple(i, y, r-1, c-1):
                    total_ways = (total_ways + dp(y, j, k-1)) % 1000000007
            return total_ways
        
        return dp(0, 0, k) % 1000000007