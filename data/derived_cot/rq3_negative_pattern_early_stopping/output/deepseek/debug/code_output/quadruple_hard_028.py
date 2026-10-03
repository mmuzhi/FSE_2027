from typing import List
from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)  # net out-degree
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = pairs[0][0]  # default if no such vertex (Eulerian circuit)
        for k in degree:
            if degree[k] == 1:
                start = k
                break

        ans = []

        def fn(x):
            """Return Eulerian path via DFS."""
            while graph[x]:
                fn(graph[x].pop())
            ans.append(x)

        fn(start)
        ans.reverse()
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]