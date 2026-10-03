class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])
        
        # Build a 2D prefix sum for the grid
        self.pref = [[0]*(self.c+1) for _ in range(self.r+1)]
        for i in range(self.r):
            for j in range(self.c):
                val = 1 if pizza[i][j]=='A' else 0
                self.pref[i+1][j+1] = val + self.pref[i][j+1] + self.pref[i+1][j] - self.pref[i][j]
        
        # Define a helper function to get the sum of a sub-pizza from (i1, j1) to (i2, j2)
        def get_sum(i1, j1, i2, j2):
            return self.pref[i2+1][j2+1] - self.pref[i1][j2+1] - self.pref[i2+1][j1] + self.pref[i1][j1]
        
        # Use memoization for getWays
        from functools import cache
        @cache
        def getWays(i, j, k):
            # The sub-pizza is from (i, j) to (self.r-1, self.c-1)
            if k == 1:
                # Check if the entire sub-pizza has at least one apple
                if get_sum(i, j, self.r-1, self.c-1) == 0:
                    return 0
                return 1
            
            total = 0
            
            # Horizontal cuts: try every row from i+1 to self.r-1
            for x in range(i+1, self.r):
                # The top part is (i, j) to (x-1, self.c-1)
                # The bottom part is (x, j) to (self.r-1, self.c-1)
                # Distribute the k-1 cuts between the two parts: top part gets t-1 cuts (split into t pieces), bottom part gets k-t cuts (split into k-t+1 pieces)
                for t in range(1, k):
                    ways_top = getWays(i, j, t)
                    ways_bottom = getWays(x, j, k-t+1)
                    total = (total + ways_top * ways_bottom) % 1000000007
            
            # Vertical cuts: try every col from j+1 to self.c-1
            for y in range(j+1, self.c):
                for t in range(1, k):
                    ways_left = getWays(i, j, t)
                    ways_right = getWays(i, y, k-t+1)
                    total = (total + ways_left * ways_right) % 0
            return total
        
        return getWays(0, 0, k) % 1000000007
