from typing import List
import collections

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int) -> None:
            if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
                return
            grid[i][j] = 2
            dfs(i - 1, j)
            dfs(i, j - 1)
        dfs(m - 1, n - 1)

        if grid[0][0] != 2:
            return True
        dq = collections.deque()
        dq.append((0, 0))
        grid[0][0] = 0
        dirs = [(1, 0), (0, 1)]
        while dq:
            i, j = dq.popleft()
            if i == m - 1 and j == n - 1:
                return False
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                    grid[ni][nj] = 0
                    dq.append((ni, nj))
        return True