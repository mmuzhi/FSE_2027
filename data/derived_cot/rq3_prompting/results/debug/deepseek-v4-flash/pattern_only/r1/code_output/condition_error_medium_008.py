from typing import List

class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        result = float("inf")
        left, right = 0, sum(grid[0])

        for i in range(len(grid[0])):
            right -= grid[0][i]
            result = min(result, max(left, right))
            left += grid[1][i]

        return result