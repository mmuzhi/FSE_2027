from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        # If the start or end is 0, then we cannot have a path (unless we can remove zeros, but we cannot)
        if grid[0][0] == 0 or grid[m-1][n-1] == 0:
            return False
        
        # Directions for BFS: right and down
        dirs = [(0, 1), (1, 0)]
        # We'll use a visited matrix or mark the grid as we go
        visited = [[False] * n for _ in range(m)]
        dq = deque()
        dq.append((0, 0))
        visited[0][0] = True
        
        while dq:
            i, j = dq.popleft()
            if i == m-1 and j == n-1:
                return True
            for dx, dy in dirs:
                ni, nj = i + dx, j + dy
                if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj] and grid[ni][nj] == 1:
                    visited[ni][nj] = True
                    dq.append((ni, nj))
        return False