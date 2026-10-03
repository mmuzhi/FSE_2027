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
            o1, o2, o3, o4 = oddDegreesNodes
            return (o1 not in neighbors[o2] and o3 not in neighbors[o4]) or \
                   (o1 not in neighbors[o3] and o2 not in neighbors[o4]) or \
                   (o1 not in neighbors[o4] and o2 not in neighbors[o3])
        elif numOdd == 2:
            o1, o2 = oddDegreesNodes
            if o1 not in neighbors[o2]:
                return True
            notConnectedTo = set(range(n)) - neighbors[o1] - neighbors[o2] - {o1, o2}
            return len(notConnectedTo) > 0
        return False