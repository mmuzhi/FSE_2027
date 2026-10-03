class Solution:
    def countPathsWithXorValue(self, grid: List[List[int]], k: int) -> int:
        m = len(grid)
        n = len(grid[0])
        mod = 10**9 + 7
        
        # dp[i][j] will be a list of 16 integers, representing the count of ways to reach (i, j) with XOR value from 0 to 15.
        # We'll use a 3D DP array: dp[i][j] is a list of 16 integers.
        dp = [[[0] * 16 for _ in range(n)] for __ in range(m)]
        
        # Base case: starting cell (0,0)
        dp[0][0][grid[0][0]] = 1
        
        # Fill the first row
        for j in range(1, n):
            for x in range(16):
                # The value from the left cell (0, j-1) must have an XOR value of x ^ grid[0][j] to make the current XOR x.
                prev_x = x ^ grid[0][j]
                dp[0][j][x] = dp[0][j-1][prev_x]
        
        # Fill the first column
        for i in range(1, m):
            for x in range(16):
                prev_x = x ^ grid[i][0]
                dp[i][0][x] = dp[i-1][0][prev_x]
        
        # Fill the rest of the grid
        for i in range(1, m):
            for j in range(1, n):
                for x in range(16):
                    # The value from the top cell (i-1, j) must have an XOR value of x ^ grid[i][j]
                    top_val = dp[i-1][j][x ^ grid[i][j]]
                    left_val = dp[i][j-1][x ^ grid[i][j]]
                    dp[i][j][x] = (top_val + left_val) % mod
        
        # The answer is the count for the bottom-right cell (m-1, n-1) with XOR value k.
        return dp[m-1][n-1][k] % mod