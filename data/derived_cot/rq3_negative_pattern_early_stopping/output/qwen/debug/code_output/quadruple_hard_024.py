from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int) # net out degree 
        for x, y in pairs: 
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1
                
        start = None
        for node, d in degree.items():
            if d == 1:
                start = node
                break
        else:
            if degree:
                start = next(iter(degree.keys()))
            # else: no nodes, so start remains None

        ans = []

        def fn(x): 
            """Return Eulerian path via dfs."""
            while graph[x]:
                # Pop an edge from x to neighbor
                neighbor = graph[x].pop()
                fn(neighbor)
            ans.append(x)
        
        if start is None and len(pairs) == 0:
            return []
        if start is None:
            # If there's no start node and there are edges, then the graph is not Eulerian. But the problem assumes Eulerian.
            # We try to start at the first node in the pairs if available, or the first node in the graph.
            if pairs:
                start = pairs[0][0]
            else:
                start = next(iter(degree.keys())) if degree else None

        fn(start)
        ans.reverse()
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]