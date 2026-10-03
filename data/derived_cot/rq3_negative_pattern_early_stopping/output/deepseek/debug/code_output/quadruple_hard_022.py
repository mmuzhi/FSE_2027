from collections import defaultdict
from typing import List

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)  # net out-degree = out - in

        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = None
        for node, net_deg in degree.items():
            if net_deg == 1:
                start = node
                break
        if start is None:
            if graph:
                start = next(iter(graph))
            else:
                return []  # empty input

        ans = []

        def dfs(node: int) -> None:
            while graph[node]:
                dfs(graph[node].pop())
            ans.append(node)

        dfs(start)
        ans.reverse()

        return [[ans[i], ans[i + 1]] for i in range(len(ans) - 1)]