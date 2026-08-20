class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        dp_row = [[False for _ in range(n)] for _ in range(n)]
        dp_col = [[False for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                v = matrix[i][j] - 1
                if dp_row[i][v] or dp_col[j][v]:
                    return False
                dp_row[i][v] = True
                dp_col[j][v] = True
        return True