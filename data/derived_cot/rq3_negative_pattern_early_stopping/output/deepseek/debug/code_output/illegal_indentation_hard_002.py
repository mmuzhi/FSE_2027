from typing import List
from collections import deque

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        cost = 0
        queue = deque()
        dirs = [(), (0, 1), (0, -1), (1, 0), (-1, 0)]

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < m and 0 <= y < n

        def dfs(x: int, y: int) -> None:
            while in_bounds(x, y) and grid[x][y] is not None:
                dx, dy = dirs[grid[x][y]]
                grid[x][y] = None  # mark visited
                queue.append((x, y))
                x, y = x + dx, y + dy

        dfs(0, 0)
        if grid[m-1][n-1] is None:
            return 0

        while queue:
            cost += 1
            q = len(queue)
            for _ in range(q):
                x, y = queue.popleft()
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if in_bounds(nx, ny) and grid[nx][ny] is not None:
                        dfs(nx, ny)
                        if grid[m-1][n-1] is None:
                            return cost
        return -1