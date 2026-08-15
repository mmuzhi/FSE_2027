from typing import List
import collections

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        # Mark cells from which the target is reachable.
        stack = [(m - 1, n - 1)]
        grid[m - 1][n - 1] = 2
        while stack:
            i, j = stack.pop()
            for di, dj in ((-1, 0), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2
                    stack.append((ni, nj))

        # BFS from the source over cells that can still reach the target.
        dq = collections.deque([(0, 0)])
        grid[0][0] = 0
        while dq:
            for _ in range(len(dq)):
                i, j = dq.popleft()
                if i == m - 1 and j == n - 1:
                    return False

                for di, dj in ((1, 0), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 2:
                        grid[ni][nj] = 0
                        dq.append((ni, nj))

            if len(dq) == 1 and dq[0] != (m - 1, n - 1):
                return True

        return True