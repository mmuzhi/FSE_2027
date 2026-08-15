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

        start = next(iter(graph))
        for node in graph:
            if degree[node] == 1:
                start = node
                break

        stack = [start]
        path = []

        while stack:
            u = stack[-1]
            if graph[u]:
                v = graph[u].pop()
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()
        return [[path[i], path[i + 1]] for i in range(len(path) - 1)]