from typing import List

class Solution:
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        neighbors = [set() for _ in range(n)]

        for a, b in edges:
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)

        odd_degree_nodes = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        num_odd = len(odd_degree_nodes)

        if num_odd == 0:
            return True

        if num_odd == 2:
            o1, o2 = odd_degree_nodes

            if o1 not in neighbors[o2]:
                return True

            both_connected_to = neighbors[o1] | neighbors[o2]
            return len(both_connected_to) < n

        if num_odd == 4:
            o1, o2, o3, o4 = odd_degree_nodes
            return (
                (o1 not in neighbors[o2] and o3 not in neighbors[o4]) or
                (o1 not in neighbors[o3] and o2 not in neighbors[o4]) or
                (o1 not in neighbors[o4] and o2 not in neighbors[o3])
            )

        return False