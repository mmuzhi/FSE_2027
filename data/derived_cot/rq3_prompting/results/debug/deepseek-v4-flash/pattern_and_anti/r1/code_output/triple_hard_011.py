from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        self.r = len(pizza)
        self.c = len(pizza[0])

        tot_apples = 0
        self.pfsum_row = []
        self.pfsum_col = []

        for i in range(self.r):
            pfr = 0
            pfs_r = [0] * self.c
            pfs_c = [0] * self.c
            for j in range(self.c):
                if i > 0:
                    pfs_c[j] += self.pfsum_col[i - 1][j]
                if pizza[i][j] == 'A':
                    pfr += 1
                    pfs_c[j] += 1
                    tot_apples += 1
                pfs_r[j] = pfr
            self.pfsum_row.append(pfs_r)
            self.pfsum_col.append(pfs_c)

        if tot_apples < k:
            return 0

        if k == 1:
            return 1

        return self.getWays(0, 0, k) % 1000000007

    @lru_cache(None)
    def getWays(self, i: int, j: int, k: int) -> int:
        if k == 1:
            for c in range(j, self.c):
                apples = self.pfsum_col[self.r - 1][c]
                if i > 0:
                    apples -= self.pfsum_col[i - 1][c]
                if apples:
                    return 1
            return 0

        total = 0

        # Horizontal cuts
        cannot_cut = True
        nr = i
        while nr < self.r - 1:
            while nr < self.r - 1 and cannot_cut:
                apples = self.pfsum_row[nr][self.c - 1]
                if j > 0:
                    apples -= self.pfsum_row[nr][j - 1]
                if apples:
                    cannot_cut = False
                else:
                    nr += 1

            if nr < self.r - 1:
                total = (total + self.getWays(nr + 1, j, k - 1)) % 1000000007
            nr += 1

        # Vertical cuts
        cannot_cut = True
        nc = j
        while nc < self.c - 1:
            while nc < self.c - 1 and cannot_cut:
                apples = self.pfsum_col[self.r - 1][nc]
                if i > 0:
                    apples -= self.pfsum_col[i - 1][nc]
                if apples:
                    cannot_cut = False
                else:
                    nc += 1

            if nc < self.c - 1:
                total = (total + self.getWays(i, nc + 1, k - 1)) % 1000000007
            nc += 1

        return total % 1000000007