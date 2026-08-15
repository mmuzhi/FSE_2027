from typing import List

class Solution:
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for a, b in edges:
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)

        odd = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        m = len(odd)

        if m == 0:
            return True

        if m == 2:
            u, v = odd
            if u not in neighbors[v]:
                return True
            return len(neighbors[u] | neighbors[v]) != n

        if m == 4:
            a, b, c, d = odd
            return ((a not in neighbors[b] and c not in neighbors[d]) or
                    (a not in neighbors[c] and b not in neighbors[d]) or
                    (a not in neighbors[d] and b not in neighbors[c]))

        return False