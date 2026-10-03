class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        n = len(grid[0])
        left0 = 0
        right1 = sum(grid[1])
        result = float('inf')
        
        for j in range(n-1):
            left0 += grid[0][j]
            right1 -= grid[1][j]
            current_cost = max(left0, right1)
            if current_cost < result:
                result = current_cost
                
        return result