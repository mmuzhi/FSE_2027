from typing import List

class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        rows = [[False] * (n + 1) for _ in range(n)]
        cols = [[False] * (n + 1) for _ in range(n)]

        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val < 1 or val > n or rows[i][val] or cols[j][val]:
                    return False
                rows[i][val] = True
                cols[j][val] = True

        return True