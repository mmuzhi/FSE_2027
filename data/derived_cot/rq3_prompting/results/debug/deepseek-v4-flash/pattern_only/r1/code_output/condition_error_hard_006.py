from collections import deque
from typing import List

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        cost = 0
        queue = deque()
        rows, cols = range(m), range(n)

        def seen(x: int, y: int) -> bool:
            return x not in rows or y not in cols or grid[x][y] is None

        directions = ((), (0, 1), (0, -1), (1, 0), (-1, 0))

        def dfs(x: int, y: int) -> None:
            while not seen(x, y):
                dx, dy = directions[grid[x][y]]
                grid[x][y] = None
                queue.append((x, y))
                x += dx
                y += dy

        dfs(0, 0)

        while queue:
            if (m - 1, n - 1) in queue:
                return cost

            cost += 1
            q = len(queue)

            for _ in range(q):
                x, y = queue.popleft()
                for dx, dy in directions[1:]:
                    dfs(x + dx, y + dy)

        return -1