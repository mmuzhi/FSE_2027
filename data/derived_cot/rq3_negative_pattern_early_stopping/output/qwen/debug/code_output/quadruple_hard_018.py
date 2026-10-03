import heapq
from typing import List

class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # Initialize distance array with a very large number
        INF = float('inf')
        dist = [[INF] * n for _ in range(m)]
        # Set the starting cell's distance to grid[0][0]
        dist[0][0] = grid[0][0]
        # Priority queue: (cost, i, j)
        pq = [(grid[0][0], 0, 0)]
        
        while pq:
            d, i, j = heapq.heappop(pq)
            if i == m - 1 and j == n - 1:
                return d
            # If we have a better distance, skip
            if d != dist[i][j]:
                continue
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    new_cost = d + grid[ni][nj]
                    if new_cost < dist[ni][nj]:
                        dist[ni][nj] = new_cost
                        heapq.heappush(pq, (new_cost, ni, nj))
        return dist[m-1][n-1]