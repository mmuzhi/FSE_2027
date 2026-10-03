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
        elif numOdd == 2:
            o1, o2 = oddDegreesNodes
            if o1 not in neighbors[o2]:
                return True
            # If they are connected, then we need to use a third node
            # But if there is no third node (n==2), then we cannot fix
            if n == 2:
                return False
            return True
        return False