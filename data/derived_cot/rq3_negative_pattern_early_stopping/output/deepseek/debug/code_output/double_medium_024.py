from typing import List
from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if m == 1 and n == 1:
            return True
        dq = deque()
        dq.append((0, 0))
        grid[0][0] = 0
        parent = [[(-1, -1) for _ in range(n)] for _ in range(m)]
        while dq:
            i, j = dq.popleft()
            if i == m - 1 and j == n - 1:
                break
            for di, dj in ((1, 0), (0, 1)):
                ni, nj = i + di, j + dj
                if ni < m and nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 0
                    parent[ni][nj] = (i, j)
                    dq.append((ni, nj))
        else:
            return False
        path = []
        i, j = m - 1, n - 1
        while i != 0 or j != 0:
            path.append((i, j))
            i, j = parent[i][j]
        path.append((0, 0))
        path.reverse()
        for i, j in path[1:-1]:
            grid[i][j] = 0
        dq = deque()
        dq.append((0, 0))
        visited = [[False] * n for _ in range(m)]
        visited[0][0] = True
        while dq:
            i, j = dq.popleft()
            if i == m - 1 and j == n - 1:
                return False
            for di, dj in ((1, 0), (0, 1)):
                ni, nj = i + di, j + dj
                if ni < m and nj < n and grid[ni][nj] == 1 and not visited[ni][nj]:
                    visited[ni][nj] = True
                    dq.append((ni, nj))
        return True