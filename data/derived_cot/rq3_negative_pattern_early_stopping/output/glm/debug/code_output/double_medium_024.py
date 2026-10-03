import collections
from typing import List

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 0 or grid[m-1][n-1] == 0: return True
        dirs = [(-1, 0), (0, -1)]
        def dfs(i: int, j: int) -> None:
            grid[i][j] = 2
            for di, dj in dirs:
                if 0 <= i + di < m and 0 <= j + dj < n and grid[i + di][j + dj] == 1: dfs(i + di, j + dj)
        
        dfs(m - 1, n - 1)
        if grid[0][0] != 2: return True
        
        dq = collections.deque([(0, 0)])
        grid[0][0] = 0
        dirs = [(1, 0), (0, 1)]
        while dq:
            if len(dq) == 1 and dq[0] != (0, 0) and dq[0] != (m - 1, n - 1): return True
            l = len(dq)
            for _ in range(l):
                i, j = dq.popleft()
                if i == m - 1 and j == n - 1: return False
                for di, dj in dirs:
                    if 0 <= i + di < m and 0 <= j + dj < n and grid[i + di][j + dj] == 2: 
                        dq.append((i + di, j + dj))
                        grid[i + di][j + dj] = 0
        return True