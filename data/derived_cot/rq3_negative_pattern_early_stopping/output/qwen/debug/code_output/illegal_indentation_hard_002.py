from collections import deque
from typing import List

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 0:
            return 0
        
        visited = [[False] * n for _ in range(m)]
        queue = deque()
        queue.append((0, 0))
        visited[0][0] = True
        cost = 0
        
        while queue:
            size = len(queue)
            for _ in range(size):
                x, y = queue.popleft()
                if x == m - 1 and y == n - 1:
                    return cost
                
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] != 0:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
            cost += 1
        
        return cost