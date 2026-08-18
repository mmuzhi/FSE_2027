class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for edge in edges:
            a, b = edge
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)
        oddDegreesNodes = [i for i in range(n) if (len(neighbors[i]) % 2 == 1)]
        numOdd = len(oddDegreesNodes)
        if numOdd == 0:
            return True
        elif numOdd == 4:
            # Only possible if the four odd nodes can be split into two non-adjacent pairs
            o1, o2, o3, o4 = oddDegreesNodes
            pairings = [((o1, o2), (o3, o4)),
                        ((o1, o3), (o2, o4)),
                        ((o1, o4), (o2, o3))]
            return any(b not in neighbors[a] and d not in neighbors[c]
                       for (a, b), (c, d) in pairings)
        elif numOdd == 2:
            # Only possible if both not connected or both connected but there is another node to connect to
            o1, o2 = oddDegreesNodes
            if o1 not in neighbors[o2]:
                # Case 1: Not connected
                return True
            # Case 2: need a node adjacent to neither o1 nor o2
            neitherConnectedTo = set(range(n)) - neighbors[o1] - neighbors[o2]
            # Oops, no other node to connect to!
            return len(neitherConnectedTo) > 0
        return False