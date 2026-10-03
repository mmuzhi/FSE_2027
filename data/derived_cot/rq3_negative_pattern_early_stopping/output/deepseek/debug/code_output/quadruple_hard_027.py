from collections import defaultdict
from typing import List

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)  # net out-degree: out - in
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = None
        for node in degree:
            if degree[node] == 1:
                start = node
                break
        if start is None:  # Eulerian circuit: start from any node with edges
            for node in graph:
                if graph[node]:
                    start = node
                    break

        ans = []

        def dfs(node):
            while graph[node]:
                dfs(graph[node].pop())
            ans.append(node)

        dfs(start)
        ans.reverse()
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]