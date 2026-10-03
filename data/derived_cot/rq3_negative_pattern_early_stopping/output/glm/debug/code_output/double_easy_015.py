from typing import List

class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        dp_row = [[False for _ in range(n + 1)] for _ in range(n)]
        dp_col = [[False for _ in range(n + 1)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if dp_row[i][val] or dp_col[j][val]:
                    return False
                dp_row[i][val] = True
                dp_col[j][val] = True
        return True