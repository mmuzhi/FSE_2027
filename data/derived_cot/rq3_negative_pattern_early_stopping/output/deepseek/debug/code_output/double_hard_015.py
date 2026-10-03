from typing import List
from functools import cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])
        self.mod = 1000000007

        self.ps = [[0] * (self.c + 1) for _ in range(self.r + 1)]
        total_apples = 0
        for i in range(self.r):
            for j in range(self.c):
                val = 1 if pizza[i][j] == 'A' else 0
                self.ps[i + 1][j + 1] = (self.ps[i][j + 1] + self.ps[i + 1][j]
                                         - self.ps[i][j] + val)
                total_apples += val

        if total_apples < k:
            return 0

        if k == 1:
            return 1

        return self.getWays(0, 0, k) % self.mod

    @cache
    def getWays(self, i: int, j: int, k: int) -> int:
        def has_apple(i, j):
            return (self.ps[self.r][self.c] - self.ps[i][self.c]
                    - self.ps[self.r][j] + self.ps[i][j]) > 0

        if k == 1:
            return 1 if has_apple(i, j) else 0

        total = 0
        for nr in range(i, self.r - 1):
            if (self.ps[nr + 1][self.c] - self.ps[i][self.c]
                - self.ps[nr + 1][j] + self.ps[i][j]) > 0:
                total += self.getWays(nr + 1, j, k - 1)

        for nc in range(j, self.c - 1):
            if (self.ps[self.r][nc + 1] - self.ps[i][nc + 1]
                - self.ps[self.r][j] + self.ps[i][j]) > 0:
                total += self.getWays(i, nc + 1, k - 1)

        return total