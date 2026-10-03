from collections import defaultdict

class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int) # net out degree 
        for x, y in pairs: 
            graph[x].append(y)
            degree[x] += 1
            degree[y] -= 1
                
        # Find the start node: the node with net out_degree 1 (if exists)
        start_node = None
        for k in degree: 
            if degree[k] == 1:
                start_node = k
                break
                
        if start_node is None:
            # If no node has out_degree 1, then we try to find a node with out_degree != 0 (for Eulerian circuit)
            # But note: the condition for Eulerian circuit is all nodes have equal in and out degree.
            # We can choose any node (say the first one) and then run DFS.
            start_node = next(iter(degree.keys()))
        
        ans = []
        # We'll define a DFS function that uses the graph and appends the node when no more edges
        def fn(x):
            while graph[x]:
                # Pop an edge from x to some neighbor
                y = graph[x].pop()
                fn(y)
            ans.append(x)
        
        fn(start_node)
        ans.reverse()
        # Convert the list of nodes to list of edges
        return [[ans[i], ans[i+1]] for i in range(len(ans)-1)]