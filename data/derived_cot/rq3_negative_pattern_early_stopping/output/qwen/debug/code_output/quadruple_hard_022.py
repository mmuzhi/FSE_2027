from collections import defaultdict
from typing import List

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        net_degree = defaultdict(int)
        for u, v in pairs:
            graph[u].append(v)
            net_degree[u] += 1
            net_degree[v] -= 1
        
        start = None
        end = None
        for node, d in net_degree.items():
            if d == 1:
                if start is None:
                    start = node
                else:
                    return []
            elif d == -1:
                if end is None:
                    end = node
                else:
                    return []
            elif d != 0:
                return []
        
        if start is None and end is None:
            nodes = list(graph.keys())
            if not nodes:
                return []
            start = nodes[0]
        elif start is None:
            return []
        elif end is None:
            return []
        
        stack = [start]
        path = []
        
        while stack:
            node = stack[-1]
            if graph[node]:
                neighbor = graph[node].pop()
                stack.append(neighbor)
            else:
                path.append(stack.pop())
        
        trail = path[::-1]
        
        if not trail:
            return []
        
        edges = []
        for i in range(len(trail) - 1):
            edges.append([trail[i], trail[i+1]])
        
        return edges