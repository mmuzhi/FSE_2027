import heapq
from typing import List

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [[float('inf')] * n for _ in range(m)]
        payed = [[False] * n for _ in range(m)]
        heap = []
        
        if grid[0][0] == 0:
            dp[0][0] = 1
            payed[0][0] = True
            heapq.heappush(heap, (1, 0, 0))
        else:
            dp[0][0] = 0
            heapq.heappush(heap, (0, 0, 0))
        
        while heap:
            cost, x, y = heapq.heappop(heap)
            if x == m-1 and y == n-1:
                return cost
            if cost != dp[x][y]:
                continue
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    if grid[nx][ny] == 0 and not payed[nx][ny]:
                        new_cost = cost + 1
                        payed[nx][ny] = True
                    else:
                        new_cost = cost
                    if new_cost < dp[nx][ny]:
                        dp[nx][ny] = new_cost
                        heapq.heappush(heap, (new_cost, nx, ny))
        return dp[m-1][n-1]