class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        m = len(grid)
        n = len(grid[0])
        result = []
        for i in range(m):
            if i % 2 == 0:
                for j in range(n):
                    if (i+j) % 2 == 0:
                        result.append(grid[i][j])
            else:
                for j in range(n-1, -1, -1):
                    if (i+j) % 2 == 0:
                        result.append(grid[i][j])
        return result