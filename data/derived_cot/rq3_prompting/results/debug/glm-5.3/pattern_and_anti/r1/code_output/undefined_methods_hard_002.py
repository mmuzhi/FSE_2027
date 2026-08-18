class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for edge in edges:
            a, b = edge
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)
        oddDegreesNodes = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        numOdd = len(oddDegreesNodes)
        if numOdd == 0:
            return True
        elif numOdd == 4:
            # Only possible if the four odd nodes can be split into two
            # non-adjacent pairs (try all three pairings)
            o1, o2, o3, o4 = oddDegreesNodes
            pairings = [
                ((o1, o2), (o3, o4)),
                ((o1, o3), (o2, o4)),
                ((o1, o4), (o2, o3)),
            ]
            for (a, b), (c, d) in pairings:
                if b not in neighbors[a] and d not in neighbors[c]:
                    return True
            return False
        elif numOdd == 2:
            o1, o2 = oddDegreesNodes
            if o1 not in neighbors[o2]:
                # Case 1: Not connected, add a single edge between them
                return True
            # Case 2: Connected, need a third node adjacent to neither
            # (note: o1 and o2 are each in the union via each other)
            connectedToEither = neighbors[o1] | neighbors[o2]
            return len(connectedToEither) < n
        return False