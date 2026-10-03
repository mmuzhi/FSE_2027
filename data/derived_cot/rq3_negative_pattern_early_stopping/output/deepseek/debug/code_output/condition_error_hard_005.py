from typing import List

class Solution:
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for a, b in edges:
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)
        
        odd_deg = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        m = len(odd_deg)
        
        if m == 0:
            return True
        if m == 2:
            u, v = odd_deg
            if v not in neighbors[u]:
                return True
            union = neighbors[u] | neighbors[v]
            if len(union) < n:
                return True
            return False
        if m == 4:
            a, b, c, d = odd_deg
            if (b not in neighbors[a] and d not in neighbors[c]):
                return True
            if (c not in neighbors[a] and d not in neighbors[b]):
                return True
            if (d not in neighbors[a] and c not in neighbors[b]):
                return True
            return False
        return False