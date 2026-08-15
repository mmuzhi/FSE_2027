from typing import List
from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        if grid[0][0] == 0 or grid[m - 1][n - 1] == 0:
            return True

        reachable = [[False] * n for _ in range(m)]
        q = deque([(0, 0)])
        reachable[0][0] = True

        while q:
            i, j = q.popleft()
            for di, dj in ((1, 0), (0, 1)):
                ni, nj = i + di, j + dj
                if ni < m and nj < n and not reachable[ni][nj] and grid[ni][nj] == 1:
                    reachable[ni][nj] = True
                    q.append((ni, nj))

        if not reachable[m - 1][n - 1]:
            return True

        can_reach_end = [[False] * n for _ in range(m)]
        q = deque([(m - 1, n - 1)])
        can_reach_end[m - 1][n - 1] = True

        while q:
            i, j = q.popleft()
            for di, dj in ((-1, 0), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and not can_reach_end[ni][nj] and reachable[ni][nj] and grid[ni][nj] == 1:
                    can_reach_end[ni][nj] = True
                    q.append((ni, nj))

        for s in range(1, m + n - 2):
            cnt = 0
            for i in range(max(0, s - (n - 1)), min(m - 1, s) + 1):
                j = s - i
                if reachable[i][j] and can_reach_end[i][j]:
                    cnt += 1
                    if cnt > 1:
                        break
            if cnt == 1:
                return True

        return False