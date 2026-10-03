class Solution:
    def restoreArray(self, adjacentPairs: List[List[int]]) -> List[int]:
        graph = {}
        for u, v in adjacentPairs: 
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, []).append(u)
        
        # If there are no edges, then the array has one node. We don't know the node, so we return [0] as a placeholder.
        if not graph:
            return [0]
        
        # Find a node with degree 1 (the ends)
        # There should be at least two nodes with degree 1 in a chain? Actually, there are exactly two.
        # But we can find any node with degree 1.
        # We'll find one.
        start_node = next(x for x in graph if len(graph[x]) == 1)
        
        ans = []
        seen = set()
        stack = [start_node]
        while stack:
            n = stack.pop()
            ans.append(n)
            seen.add(n)
            for nn in graph[n]:
                if nn not in seen:
                    stack.append(nn)
        return ans