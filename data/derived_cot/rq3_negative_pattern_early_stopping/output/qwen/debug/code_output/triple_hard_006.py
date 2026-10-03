from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int) # net out degree (out_degree - in_degree)
        for x, y in pairs:
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1

        # Check the conditions for Eulerian path
        start = None
        end = None
        for node, d in degree.items():
            if d == 1:
                start = node
            elif d == -1:
                end = node
            # If we find a node with absolute value not 1, then it's invalid
            elif d != 0:
                return []  # Not an Eulerian path

        # If there's no start or end, then it's an Eulerian cycle
        if start is None and end is None:
            # We can choose any node as start, let's choose the first node in the graph
            start = next(iter(graph.keys())) if graph else None
        elif start is None:
            # This should not happen because if there's an end, there must be a start? 
            # Actually, the condition above would have caught if there's a node with non-zero and not 1 or -1.
            return []
        elif end is None:
            return []

        # We'll use DFS to traverse the graph starting from `start`
        ans = []
        # We need to define a DFS function that uses the graph and appends to ans
        def dfs(x):
            while graph[x]:
                neighbor = graph[x].pop()
                dfs(neighbor)
            ans.append(x)

        dfs(start)
        ans.reverse()
        # The answer should be a list of edges: [ [ans[0], ans[1]], [ans[1], ans[2]], ... ]
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]