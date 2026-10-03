class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for a, b in edges:
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)
        
        odd_degree_nodes = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        m = len(odd_degree_nodes)
        
        if m == 0:
            return True
        if m == 2:
            u, v = odd_degree_nodes
            return v not in neighbors[u]
        if m == 4:
            a, b, c, d = odd_degree_nodes
            if b not in neighbors[a] and d not in neighbors[c]:
                return True
            if c not in neighbors[a] and d not in neighbors[b]:
                return True
            if d not in neighbors[a] and c not in neighbors[b]:
                return True
            return False
        return False