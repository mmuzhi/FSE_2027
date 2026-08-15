from typing import List

class Solution:
    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        for row in grid:
            row.sort()
        
        ans = 0
        for j in range(len(grid[0]) - 1, -1, -1):
            max_val = 0
            for row in grid:
                max_val = max(max_val, row[j])
            ans += max_val
        
        return ans