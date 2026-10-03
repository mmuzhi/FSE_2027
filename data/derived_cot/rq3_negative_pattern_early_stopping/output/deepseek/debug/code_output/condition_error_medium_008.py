from typing import List

class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        top_sum = sum(grid[0])
        bottom_sum = 0
        result = float('inf')
        for i in range(len(grid[0])):
            top_sum -= grid[0][i]
            result = min(result, max(top_sum, bottom_sum))
            bottom_sum += grid[1][i]
        return result