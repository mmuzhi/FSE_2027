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
            start = next(iter(graph.keys())) if graph else None
        
        ans = []
        
        def dfs(node):
            while graph[node]:
                neighbor = graph[node].pop()
                dfs(neighbor)
            ans.append(node)
        
        if start is not None:
            dfs(start)
        
        ans.reverse()
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]