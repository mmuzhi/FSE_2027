from typing import List

class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        result = float("inf")
        left, right = 0, sum(grid[0])

        for bottom_cell, top_cell in zip(grid[1], grid[0]):
            right -= top_cell
            result = min(result, max(left, right))
            left += bottom_cell

        return result