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

        if m == 4:
            o1, o2, o3, o4 = odd
            return ((o1 not in neighbors[o2] and o3 not in neighbors[o4]) or
                    (o1 not in neighbors[o3] and o2 not in neighbors[o4]) or
                    (o1 not in neighbors[o4] and o2 not in neighbors[o3]))

        if m == 2:
            o1, o2 = odd
            if o1 not in neighbors[o2]:
                return True

            connected_to_either = neighbors[o1] | neighbors[o2]
            return len(connected_to_either) < n

        return False