from typing import List
import collections

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 0 or grid[m-1][n-1] == 0:
            return True

        dirs = [(1,0), (0,1)]
        path = []
        found = False

        def dfs(i, j):
            nonlocal found
            if found:
                return
            if i == m-1 and j == n-1:
                path.append((i,j))
                found = True
                return
            if grid[i][j] == 0:
                return
            grid[i][j] = 0  # mark visited
            path.append((i,j))
            for di, dj in dirs:
                ni, nj = i+di, j+dj
                if 0 <= ni < m and 0 <= nj < n:
                    dfs(ni, nj)
                    if found:
                        return
            if not found:
                path.pop()

        dfs(0, 0)

        if not found:
            return True   # already disconnected

        for x, y in path:
            if (x, y) == (0, 0) or (x, y) == (m-1, n-1):
                continue  # we can return True immediately, but let's handle generically.
                pass

            original = grid[x][y]
            grid[x][y] = 0
            dq = collections.deque()
            dq.append((0,0))
            visited = [[False]*n for _ in range(m)]
            visited[0][0] = True
            reachable = False
            while dq:
                i, j = dq.popleft()
                if i == m-1 and j == n-1:
                    reachable = True
                    break
                for di, dj in dirs:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1 and not visited[ni][nj]:
                        visited[ni][nj] = True
                        dq.append((ni, nj))
            if not reachable:
                return True
            grid[x][y] = original

        return False