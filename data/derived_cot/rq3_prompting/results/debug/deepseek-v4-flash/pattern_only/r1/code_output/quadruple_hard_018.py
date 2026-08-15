from typing import List
from collections import deque

class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[float('inf')] * n for _ in range(m)]
        dist[0][0] = 0
        q = deque([(0, 0, 0)])

        while q:
            d, i, j = q.popleft()
            if d != dist[i][j]:
                continue
            if i == m - 1 and j == n - 1:
                return d

            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    nd = d + grid[ni][nj]
                    if nd < dist[ni][nj]:
                        dist[ni][nj] = nd
                        if grid[ni][nj] == 1:
                            q.append((nd, ni, nj))
                        else:
                            q.appendleft((nd, ni, nj))

        return dist[m - 1][n - 1]