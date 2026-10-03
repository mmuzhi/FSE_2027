from typing import List
from collections import deque

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        cost = 0
        queue = deque()
        M, N = range(m), range(n)

        seen = lambda x, y: x not in M or y not in N or grid[x][y] is None
        dir = ((), (0, 1), (0, -1), (1, 0), (-1, 0))

        def dfs(x: int, y: int) -> None:
            while not seen(x, y):
                (dx, dy), grid[x][y] = dir[grid[x][y]], None
                queue.append((x, y))
                x, y = x + dx, y + dy

        dfs(0, 0)

        while queue:
            if (m - 1, n - 1) in queue:
                return cost
            cost += 1
            q = len(queue)
            for _ in range(q):
                x, y = queue.popleft()
                for dx, dy in dir[1:]:
                    dfs(x + dx, y + dy)

        return -1  # fallback (should not be reached)