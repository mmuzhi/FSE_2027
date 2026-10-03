import collections

class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        distance = [[float('inf')] * n for _ in range(m)]
        distance[0][0] = 0
        q = collections.deque()
        q.append((0, 0, 0))
        
        while q:
            d, i, j = q.popleft()
            if i == m - 1 and j == n - 1:
                return d
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    new_d = d + grid[ni][nj]
                    if new_d < distance[ni][nj]:
                        distance[ni][nj] = new_d
                        if grid[ni][nj] == 0:
                            q.appendleft((new_d, ni, nj))
                        else:
                            q.append((new_d, ni, nj))
        return distance[m-1][n-1]