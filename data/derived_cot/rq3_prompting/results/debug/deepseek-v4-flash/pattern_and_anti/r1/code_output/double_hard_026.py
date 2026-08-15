class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for a, b in edges:
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)

        odd = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        num_odd = len(odd)

        if num_odd == 0:
            return True

        if num_odd == 2:
            o1, o2 = odd
            if o1 not in neighbors[o2]:
                return True
            for x in range(n):
                if x not in neighbors[o1] and x not in neighbors[o2]:
                    return True
            return False

        if num_odd == 4:
            o1, o2, o3, o4 = odd
            if o1 not in neighbors[o2] and o3 not in neighbors[o4]:
                return True
            if o1 not in neighbors[o3] and o2 not in neighbors[o4]:
                return True
            if o1 not in neighbors[o4] and o2 not in neighbors[o3]:
                return True
            return False

        return False