from typing import List

class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        for i in range(n):
            seen = [False] * (n + 1)
            for j in range(n):
                val = matrix[i][j]
                if val < 1 or val > n or seen[val]:
                    return False
                seen[val] = True
        for j in range(n):
            seen = [False] * (n + 1)
            for i in range(n):
                val = matrix[i][j]
                if val < 1 or val > n or seen[val]:
                    return False
                seen[val] = True
        return True