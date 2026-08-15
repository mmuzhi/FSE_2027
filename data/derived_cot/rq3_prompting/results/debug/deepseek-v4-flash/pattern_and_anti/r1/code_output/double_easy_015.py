from typing import List

class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)

        for i in range(n):
            row_seen = [False] * (n + 1)
            col_seen = [False] * (n + 1)

            for j in range(n):
                rv = matrix[i][j]
                cv = matrix[j][i]

                if rv < 1 or rv > n or cv < 1 or cv > n:
                    return False

                if row_seen[rv] or col_seen[cv]:
                    return False

                row_seen[rv] = True
                col_seen[cv] = True

        return True