from typing import List
from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)

        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = None
        for node, d in degree.items():
            if d == 1:
                start = node
                break

        if start is None:
            start = next(iter(graph), None)

        if start is None:
            return []

        ans = []
        stack = [start]

        while stack:
            u = stack[-1]
            if graph[u]:
                stack.append(graph[u].pop())
            else:
                ans.append(stack.pop())

        ans.reverse()
        return [[ans[i], ans[i + 1]] for i in range(len(ans) - 1)]