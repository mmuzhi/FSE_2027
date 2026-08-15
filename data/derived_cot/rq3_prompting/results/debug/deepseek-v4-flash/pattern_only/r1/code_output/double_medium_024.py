from typing import List

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        reach_start = [[False] * n for _ in range(m)]
        reach_start[0][0] = grid[0][0] == 1
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    continue
                if i == 0 and j == 0:
                    continue
                if (i > 0 and reach_start[i - 1][j]) or (j > 0 and reach_start[i][j - 1]):
                    reach_start[i][j] = True

        reach_end = [[False] * n for _ in range(m)]
        reach_end[m - 1][n - 1] = grid[m - 1][n - 1] == 1
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 0:
                    continue
                if i == m - 1 and j == n - 1:
                    continue
                if (i + 1 < m and reach_end[i + 1][j]) or (j + 1 < n and reach_end[i][j + 1]):
                    reach_end[i][j] = True

        if not reach_start[m - 1][n - 1]:
            return True

        diag_count = [0] * (m + n - 1)
        for i in range(m):
            for j in range(n):
                if reach_start[i][j] and reach_end[i][j]:
                    diag_count[i + j] += 1

        for s in range(1, m + n - 2):
            if diag_count[s] == 1:
                return True

        return False