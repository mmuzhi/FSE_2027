class Disjoint:
    def __init__(self, n=26):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def finduPar(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.finduPar(self.parent[node])
        return self.parent[node]

    def union(self, u, v):
        ru = self.finduPar(u)
        rv = self.finduPar(v)
        if ru == rv:
            return
        if self.rank[ru] < self.rank[rv]:
            self.parent[ru] = rv
        elif self.rank[ru] > self.rank[rv]:
            self.parent[rv] = ru
        else:
            self.parent[rv] = ru
            self.rank[ru] += 1

class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        disjoint = Disjoint()
        nq = []
        n = len(equations)
        for i in range(n):
            if equations[i][1]=='!':
                if equations[i][0]==equations[i][-1]:
                    return False
                else:
                    nq.append(equations[i])
            else:
                u = ord(equations[i][0]) - 97
                v = ord(equations[i][-1]) - 97
                disjoint.union(u, v)
        for i in range(len(nq)):
            x = ord(nq[i][0]) - 97
            y = ord(nq[i][-1]) - 97
            if disjoint.finduPar(x) == disjoint.finduPar(y):
                return False
        return True