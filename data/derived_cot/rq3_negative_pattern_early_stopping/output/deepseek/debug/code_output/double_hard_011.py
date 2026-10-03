from typing import List
import collections

class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        distance = [[float('inf') for _ in range(n)] for _ in range(m)]
        distance[0][0] = 0
        q = collections.deque([(0, 0, 0)])  # (d, i, j)
        while q:
            d, i, j = q.popleft()
            if i == m - 1 and j == n - 1:
                return d
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ci, cj = i + di, j + dj
                if 0 <= ci < m and 0 <= cj < n:
                    nd = d + grid[ci][cj]
                    if nd < distance[ci][cj]:
                        distance[ci][cj] = nd
                        if grid[ci][cj] == 1:
                            q.append((nd, ci, cj))
                        else:
                            q.appendleft((nd, ci, cj))
        return distance[m - 1][n - 1]