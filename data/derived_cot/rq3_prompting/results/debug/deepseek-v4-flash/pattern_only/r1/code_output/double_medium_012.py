from typing import List
from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        if grid[0][0] != 1 or grid[m - 1][n - 1] != 1:
            return True

        stack = [(m - 1, n - 1)]
        grid[m - 1][n - 1] = 2

        while stack:
            i, j = stack.pop()
            for di, dj in ((-1, 0), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2
                    stack.append((ni, nj))

        q = deque([(0, 0)])
        grid[0][0] = 0
        dirs = ((1, 0), (0, 1))

        while q:
            level_size = len(q)

            for _ in range(level_size):
                i, j = q.popleft()

                if i == m - 1 and j == n - 1:
                    return False

                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                        grid[ni][nj] = 0
                        q.append((ni, nj))

            if len(q) == 1 and q[0] != (m - 1, n - 1):
                return True

        return True