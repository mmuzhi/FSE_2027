from typing import List
from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int) -> None:
            grid[i][j] = 2
            for di, dj in [(-1, 0), (0, -1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    dfs(ni, nj)

        if grid[m-1][n-1] == 1:
            dfs(m-1, n-1)

        dq = deque([(0, 0)])
        grid[0][0] = 0
        dirs = [(1, 0), (0, 1)]

        while dq:
            l = len(dq)
            for _ in range(l):
                i, j = dq.popleft()
                if i == m - 1 and j == n - 1:
                    return False
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                        dq.append((ni, nj))
                        grid[ni][nj] = 0
            if len(dq) == 1 and dq[0] != (m - 1, n - 1):
                return True

        return True