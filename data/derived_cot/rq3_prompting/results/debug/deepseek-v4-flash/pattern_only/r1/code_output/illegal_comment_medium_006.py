from typing import List

class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        M = len(grid)
        if M < 3:
            return 0
        N = len(grid[0])
        if N < 3:
            return 0

        def is_magic(r: int, c: int) -> bool:
            seen = set()
            for dr in range(3):
                for dc in range(3):
                    val = grid[r + dr][c + dc]
                    if val < 1 or val > 9 or val in seen:
                        return False
                    seen.add(val)

            return (
                grid[r][c] + grid[r][c + 1] + grid[r][c + 2] == 15 and
                grid[r + 1][c] + grid[r + 1][c + 1] + grid[r + 1][c + 2] == 15 and
                grid[r + 2][c] + grid[r + 2][c + 1] + grid[r + 2][c + 2] == 15 and
                grid[r][c] + grid[r + 1][c] + grid[r + 2][c] == 15 and
                grid[r][c + 1] + grid[r + 1][c + 1] + grid[r + 2][c + 1] == 15 and
                grid[r][c + 2] + grid[r + 1][c + 2] + grid[r + 2][c + 2] == 15 and
                grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2] == 15 and
                grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c] == 15
            )

        ans = 0
        for i in range(M - 2):
            for j in range(N - 2):
                if is_magic(i, j):
                    ans += 1
        return ans