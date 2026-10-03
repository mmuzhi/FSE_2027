from typing import List

class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        M, N = len(grid), len(grid[0])
        res = 0

        def is_magic(r, c):
            nums = set()
            for i in range(3):
                for j in range(3):
                    num = grid[r + i][c + j]
                    if num < 1 or num > 9:
                        return False
                    nums.add(num)
            if len(nums) != 9:
                return False

            target = 15
            for i in range(3):
                if grid[r + i][c] + grid[r + i][c + 1] + grid[r + i][c + 2] != target:
                    return False
                if grid[r][c + i] + grid[r + 1][c + i] + grid[r + 2][c + i] != target:
                    return False
            if grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2] != target:
                return False
            if grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c] != target:
                return False
            return True

        for i in range(M - 2):
            for j in range(N - 2):
                if is_magic(i, j):
                    res += 1

        return res