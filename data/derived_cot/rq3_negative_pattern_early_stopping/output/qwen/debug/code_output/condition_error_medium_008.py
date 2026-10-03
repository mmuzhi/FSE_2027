class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        n = len(grid[0])
        left_max = [0] * n
        right_max = [0] * n
        
        left_max[0] = grid[0][0]
        for i in range(1, n):
            left_max[i] = max(left_max[i-1], grid[0][i])
        
        right_max[n-1] = grid[1][n-1]
        for i in range(n-2, -1, -1):
            right_max[i] = max(right_max[i+1], grid[1][i])
        
        ans = float('inf')
        for i in range(n):
            candidate = max(left_max[i], right_max[i])
            if candidate < ans:
                ans = candidate
                
        return ans