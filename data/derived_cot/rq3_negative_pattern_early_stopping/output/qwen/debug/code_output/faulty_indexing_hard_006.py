class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        self.r = len(pizza)
        self.c = len(pizza[0])
        self.grid = [[1 if ch == 'A' else 0 for ch in row] for row in pizza]
        self.pref = [[0]*(self.c+1) for _ in range(self.r+1)]
        for i in range(1, self.r+1):
            for j in range(1, self.c+1):
                self.pref[i][j] = self.pref[i-1][j] + self.pref[i][j-1] - self.pref[i-1][j-1] + self.grid[i-1][j-1]
        
        @cache
        def dp(i, j, k):
            # i: start row, j: start col, k: remaining cuts
            if k == 0:
                # Check if the sub-pizza from (i, j) to (self.r-1, self.c-1) has at least one apple
                total = self.pref[self.r][self.c] - self.pref[i][self.c] - self.pref[self.r][j] + self.pref[i][j]
                if total == 0:
                    return 0
                return 1
            ways = 0
            # Try horizontal cuts
            for cut_row in range(i+1, self.r):
                # Check if cutting at cut_row is valid: the piece above (from i to cut_row-1) has at least one apple
                top_total = self.pref[cut_row][self.c] - self.pref[i][self.c] - self.pref[cut_row][j] + self.pref[i][j]
                if top_total == 0:
                    continue
                # Check the piece below (from cut_row to self.r-1)
                bottom_total = self.pref[self.r][self.c] - self.pref[cut_row][self.c] - self.pref[self.r][j] + self.pref[cut_row][j]
                if bottom_total == 0:
                    continue
                ways = (ways + dp(i, j, k-1) * dp(cut_row, j, k-1)) % MOD
            # Try vertical cuts
            for cut_col in range(j+1, self.c):
                # Check if cutting at cut_col is valid: the piece left (from j to cut_col-1) has at least one apple
                left_total = self.pref[self.r][cut_col] - self.pref[i][cut_col] - self.pref[self.r][j] + self.pref[i][j]
                if left_total == 0:
                    continue
                # Check the piece right (from cut_col to self.c-1)
                right_total = self.pref[self.r][self.c] - self.pref[self.r][cut_col] - self.pref[self.r][j] + self.pref[self.r][j]
                if right_total == 0:
                    continue
                ways = (ways + dp(i, j, k-1) * dp(i, cut_col, k-1)) % MOD
            return ways
        
        return dp(0, 0, k) % MOD
