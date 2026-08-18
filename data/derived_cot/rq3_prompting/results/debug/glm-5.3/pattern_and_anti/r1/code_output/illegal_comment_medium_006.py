from typing import List


class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        M, N = len(grid), len(grid[0])
        res = 0

        solution = [
            ((4, 9, 2), (3, 5, 7), (8, 1, 6)),
            ((8, 1, 6), (3, 5, 7), (4, 9, 2)),
            ((2, 9, 4), (7, 5, 3), (6, 1, 8)),
            ((6, 1, 8), (7, 5, 3), (2, 9, 4)),
            ((4, 3, 8), (9, 5, 1), (2, 7, 6)),
            ((8, 3, 4), (1, 5, 9), (6, 7, 2)),
            ((2, 7, 6), (9, 5, 1), (4, 3, 8)),
            ((6, 7, 2), (1, 5, 9), (8, 3, 4)),
        ]

        for i in range(M - 2):
            for j in range(N - 2):
                arr = []

                for k in range(3):
                    if i + k >= M:
                        break
                    arr.append(tuple(grid[i + k][j:j + 3]))

                if tuple(arr) in solution:
                    res += 1
                else:
                    arr = [row[::-1] for row in arr]

                    if tuple(arr) in solution:
                        res += 1

        return res