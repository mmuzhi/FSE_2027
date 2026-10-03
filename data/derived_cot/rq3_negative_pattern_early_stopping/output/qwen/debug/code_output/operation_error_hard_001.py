class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        # Build a grid of apples (1 for 'A', 0 for '.')
        grid = [[0]*self.c for _ in range(self.r)]
        for i in range(self.r):
            for j in range(self.c):
                if pizza[i][j] == 'A':
                    grid[i][j] = 1
        
        # Build a 2D prefix sum array of size (r+1) x (c+1)
        self.pref = [[0]*(self.c+1) for _ in range(self.r+1)]
        for i in range(self.r):
            for j in range(self.c):
                self.pref[i+1][j+1] = self.pref[i][j+1] + self.pref[i+1][j] - self.pref[i][j] + grid[i][j]
        
        # Define a helper function to get the sum of a region [r1, r2] x [c1, c2] (inclusive)
        def get_sum(r1, c1, r2, c2):
            # r1, r2, c1, c2 are inclusive
            return self.pref[r2+1][c2+1] - self.pref[r1][c2+1] - self.pref[r2+1][c1] + self.pref[r1][c1]
        
        # If the entire pizza has no apple, return 0
        if get_sum(0, 0, self.r-1, self.c-1) == 0:
            return 0
        
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dfs(r1, c1, r2, c2, k):
            if k == 0:
                if get_sum(r1, c1, r2, c2) >= 1:
                    return 1
                return 0
            
            total = 0
            # Horizontal cuts
            for i in range(r1, r2):
                top = get_sum(r1, c1, i, c2)
                bottom = get_sum(i+1, c1, r2, c2)
                if top >= 1 and bottom >= 1:
                    total = (total + dfs(r1, c1, i, c2, k-1) * dfs(i+1, c1, r2, c2, k-1)) % 1000000007
            
            # Vertical cuts
            for j in range(c1, c2):
                left = get_sum(r1, c1, r2, j)
                right = get_sum(r1, j+1, r2, c2)
                if left >= 1 and right >= 1:
                    total = (total + dfs(r1, c1, r2, j, k-1) * dfs(r1, j+1, r2, c2, k-1)) % 1000000007
            
            return total % 1000000007
        
        result = dfs(0, 0, self.r-1, self.c-1, k) % 1000000007
        return result