class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        # If the start or end is blocked, then no path exists, so we can cut (but note: we cannot cut start/end, but if they are blocked then we don't need to cut)
        if grid[0][0] == 0 or grid[m-1][n-1] == 0:
            return True
        
        # We'll do two BFS/DFS: one from start (0,0) and one from end (m-1, n-1) in reverse directions.
        # First, mark all cells reachable from (0,0) using right and down.
        visited1 = [[False] * n for _ in range(m)]
        dq = deque([(0, 0)])
        visited1[0][0] = True
        while dq:
            i, j = dq.popleft()
            for di, dj in [(1, 0), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and not visited1[ni][nj] and grid[ni][nj] == 1:
                    visited1[ni][nj] = True
                    dq.append((ni, nj))
        
        # If the end is not reachable from start, then we can cut (return True)
        if not visited1[m-1][n-1]:
            return True
        
        # Second, mark all cells reachable from (m-1, n-1) using left and up.
        visited2 = [[False] * n for _ in range(m)]
        dq = deque([(m-1, n-1)])
        visited2[m-1][n-1] = True
        while dq:
            i, j = dq.popleft()
            for di, dj in [(-1, 0), (0, -1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and not visited2[ni][nj] and grid[ni][nj] == 1:
                    visited2[ni][nj] = True
                    dq.append((ni, nj))
        
        # Now, check if there is any cell (other than start and end) that is common in both visited1 and visited2.
        # If there is no common cell (other than start and end), then we can cut the path (return True). Otherwise, we cannot (return False).
        for i in range(m):
            for j in range(n):
                # Skip start and end
                if (i == 0 and j == 0) or (i == m-1 and j == n-1):
                    continue
                if visited1[i][j] and visited2[i][j]:
                    return False
        
        return True
