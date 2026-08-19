class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        neighbors = [set() for _ in range(n)]
        for edge in edges:
            a, b = edge
            a -= 1
            b -= 1
            neighbors[a].add(b)
            neighbors[b].add(a)

        oddDegreeNodes = [i for i in range(n) if len(neighbors[i]) % 2 == 1]
        numOdd = len(oddDegreeNodes)

        if numOdd == 0:
            return True
        elif numOdd == 4:
            # Need two disjoint pairs of odd nodes that are not adjacent
            o1, o2, o3, o4 = oddDegreeNodes

            def notConnected(x, y):
                return x not in neighbors[y]

            return ((notConnected(o1, o2) and notConnected(o3, o4)) or
                    (notConnected(o1, o3) and notConnected(o2, o4)) or
                    (notConnected(o1, o4) and notConnected(o2, o3)))
        elif numOdd == 2:
            o1, o2 = oddDegreeNodes
            if o1 not in neighbors[o2]:
                # Case 1: connect the two odd nodes directly
                return True
            # Case 2: need a helper node c adjacent to neither o1 nor o2
            for c in range(n):
                if c != o1 and c != o2 and c not in neighbors[o1] and c not in neighbors[o2]:
                    return True
            return False
        return False