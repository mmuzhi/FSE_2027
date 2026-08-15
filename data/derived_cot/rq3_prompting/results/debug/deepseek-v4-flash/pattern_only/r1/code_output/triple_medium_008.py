from typing import List

class Disjoint:
    def __init__(self):
        self.rank = [0] * 26
        self.parent = list(range(26))

    def finduPar(self, node):
        if self.parent[node] == node:
            return node
        self.parent[node] = self.finduPar(self.parent[node])
        return self.parent[node]

    def byrank(self, u, v):
        ulp_u = self.finduPar(u)
        ulp_v = self.finduPar(v)
        if ulp_u == ulp_v:
            return False
        if self.rank[ulp_u] > self.rank[ulp_v]:
            self.parent[ulp_v] = ulp_u
        elif self.rank[ulp_u] < self.rank[ulp_v]:
            self.parent[ulp_u] = ulp_v
        else:
            self.parent[ulp_v] = ulp_u
            self.rank[ulp_u] += 1
        return True

class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        dsu = Disjoint()
        not_equal = []

        for eq in equations:
            if eq[1] == '!':
                if eq[0] == eq[-1]:
                    return False
                not_equal.append(eq)
            else:
                dsu.byrank(ord(eq[0]) - ord('a'), ord(eq[-1]) - ord('a'))

        for eq in not_equal:
            x = ord(eq[0]) - ord('a')
            y = ord(eq[-1]) - ord('a')
            if dsu.finduPar(x) == dsu.finduPar(y):
                return False

        return True