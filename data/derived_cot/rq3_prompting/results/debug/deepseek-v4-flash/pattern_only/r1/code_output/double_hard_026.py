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
        elif numOdd == 2:
            o1, o2 = oddDegreesNodes
            if o1 not in neighbors[o2]:
                return True
            for x in range(n):
                if x != o1 and x != o2 and x not in neighbors[o1] and x not in neighbors[o2]:
                    return True
            return False
        elif numOdd == 4:
            o1, o2, o3, o4 = oddDegreesNodes
            if o2 not in neighbors[o1] and o4 not in neighbors[o3]:
                return True
            if o3 not in neighbors[o1] and o4 not in neighbors[o2]:
                return True
            if o4 not in neighbors[o1] and o3 not in neighbors[o2]:
                return True
            return False

        return False