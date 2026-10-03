from typing import List
import collections

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int) -> None:
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != 1:
                return
            grid[i][j] = 2
            dfs(i - 1, j)
            dfs(i, j - 1)
        dfs(m - 1, n - 1)
        if grid[0][0] != 2:
            return False
        dq = collections.deque()
        dq.append((0, 0))
        grid[0][0] = 0
        dirs = [(1, 0), (0, 1)]
        while dq:
            if len(dq) == 1 and dq[0] != (0, 0) and dq[0] != (m - 1, n - 1):
                return True
            l = len(dq)
            for _ in range(l):
                i, j = dq.popleft()
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                        dq.append((ni, nj))
                        grid[ni][nj] = 0
        return False