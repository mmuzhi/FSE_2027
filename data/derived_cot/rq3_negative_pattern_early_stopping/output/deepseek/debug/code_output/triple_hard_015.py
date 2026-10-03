from collections import defaultdict
from typing import List

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)  # net out degree
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = pairs[0][0]  # default start if no node with out-degree 1
        for k in degree:
            if degree[k] == 1:
                start = k
                break

        ans = []

        def dfs(x):
            """Return Eulerian path via dfs."""
            while graph[x]:
                dfs(graph[x].pop())
            ans.append(x)

        dfs(start)
        ans.reverse()
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]