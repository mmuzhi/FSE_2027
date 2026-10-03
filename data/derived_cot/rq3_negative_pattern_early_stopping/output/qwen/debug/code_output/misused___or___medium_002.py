import collections

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 1 or grid[m-1][n-1] == 1:
            return False
        
        stack = [(m-1, n-1)]
        grid[m-1][n-1] = 2
        while stack:
            i, j = stack.pop()
            for di, dj in [(-1,0), (0,-1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 0:
                    grid[ni][nj] = 2
                    stack.append((ni, nj))
        
        dq = collections.deque()
        if grid[0][0] == 0:
            dq.append((0, 0))
        else:
            return False
        
        while dq:
            i, j = dq.popleft()
            if i == m-1 and j == n-1:
                return True
            for di, dj in [(1,0), (0,1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 0:
                    dq.append((ni, nj))
        
        return False