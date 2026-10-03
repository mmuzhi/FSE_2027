from collections import deque
from typing import List

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n, cost, queue = len(grid), len(grid[0]), 0, deque()
        dir = ((), (0, 1), (0, -1), (1, 0), (-1, 0))

        def dfs(x: int, y: int) -> None:
            while 0 <= x < m and 0 <= y < n and grid[x][y]:
                (dx, dy), grid[x][y] = dir[grid[x][y]], None
                queue.append((x, y))
                x, y = x + dx, y + dy
            return

        dfs(0, 0)

        while queue:
            q = len(queue)
            for _ in range(q):
                x, y = queue.popleft()
                if x == m - 1 and y == n - 1:
                    return cost
                for dx, dy in dir[1:]:
                    dfs(x + dx, y + dy)
            cost += 1