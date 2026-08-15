from typing import List
from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        stack = [(m - 1, n - 1)]
        while stack:
            i, j = stack.pop()
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != 1:
                continue
            grid[i][j] = 2
            stack.append((i - 1, j))
            stack.append((i, j - 1))

        if grid[0][0] != 2:
            return True

        q = deque([(0, 0)])
        grid[0][0] = 0
        dirs = [(1, 0), (0, 1)]

        while q:
            if len(q) == 1 and q[0] != (0, 0) and q[0] != (m - 1, n - 1):
                return True

            layer_size = len(q)
            for _ in range(layer_size):
                i, j = q.popleft()
                if i == m - 1 and j == n - 1:
                    return False

                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                        q.append((ni, nj))
                        grid[ni][nj] = 0

        return True