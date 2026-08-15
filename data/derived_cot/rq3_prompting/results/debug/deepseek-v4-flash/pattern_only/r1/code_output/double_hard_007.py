from typing import List
from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        if not pairs:
            return []

        graph = defaultdict(list)
        degree = defaultdict(int)

        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        start = next((k for k in degree if degree[k] == 1), None)
        if start is None:
            start = next(iter(graph))

        ans = []
        stack = [start]

        while stack:
            node = stack[-1]
            if graph[node]:
                stack.append(graph[node].pop())
            else:
                ans.append(stack.pop())

        ans.reverse()
        return [[ans[i], ans[i + 1]] for i in range(len(ans) - 1)]