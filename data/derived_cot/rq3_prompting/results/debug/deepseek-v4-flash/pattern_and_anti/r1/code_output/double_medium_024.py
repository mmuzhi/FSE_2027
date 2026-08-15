from typing import List

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        def dfs(i: int, j: int) -> bool:
            stack = [(i, j)]
            while stack:
                x, y = stack.pop()
                if x >= m or y >= n or grid[x][y] == 0:
                    continue
                if x == m - 1 and y == n - 1:
                    return True
                grid[x][y] = 0
                stack.append((x, y + 1))
                stack.append((x + 1, y))
            return False

        if not dfs(0, 0):
            return True

        grid[0][0] = 1
        return not dfs(0, 0)