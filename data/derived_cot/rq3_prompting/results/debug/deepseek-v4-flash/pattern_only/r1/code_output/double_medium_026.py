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
        disjoint = Disjoint()
        nq = []

        for eq in equations:
            if eq[1] == '!':
                if eq[0] == eq[-1]:
                    return False
                nq.append(eq)
            else:
                disjoint.byrank(ord(eq[0]) - 97, ord(eq[-1]) - 97)

        for eq in nq:
            x = ord(eq[0]) - 97
            y = ord(eq[-1]) - 97
            if disjoint.finduPar(x) == disjoint.finduPar(y):
                return False

        return True