from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        if not pairs:
            return []
        
        graph = defaultdict(list)
        net_degree = defaultdict(int)
        
        for x, y in pairs:
            graph[x].append(y)
            net_degree[x] += 1
            net_degree[y] -= 1
        
        start = None
        end = None
        for node, d in net_degree.items():
            if d == 1:
                if start is not None:
                    return []
                start = node
            elif d == -1:
                if end is not None:
                    return []
                end = node
            elif d != 0:
                return []
        
        if start is None and end is None:
            nodes = list(graph.keys())
            if not nodes:
                return []
            start = nodes[0]
        elif start is None or end is None:
            return []
        
        ans = []
        def dfs(node):
            while graph[node]:
                neighbor = graph[node].pop()
                dfs(neighbor)
            ans.append(node)
        
        dfs(start)
        ans.reverse()
        
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]