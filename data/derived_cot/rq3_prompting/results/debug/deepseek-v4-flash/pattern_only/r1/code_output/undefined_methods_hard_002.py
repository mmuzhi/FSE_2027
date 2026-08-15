class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
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
            a, b = odd
            if b not in neighbors[a]:
                return True
            return len(neighbors[a] | neighbors[b]) < n

        if m == 4:
            a, b, c, d = odd
            if ((b not in neighbors[a] and d not in neighbors[c]) or
                (c not in neighbors[a] and d not in neighbors[b]) or
                (d not in neighbors[a] and c not in neighbors[b])):
                return True

        return False