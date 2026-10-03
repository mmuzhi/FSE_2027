class Solution:
    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        for i in range(0, len(grid)):
            grid[i].sort()
        n = len(grid[0])
        res = 0
        for j in range(0, n):
            for i in range(0, len(grid)):
                res += grid[i].pop(-j)
        return res