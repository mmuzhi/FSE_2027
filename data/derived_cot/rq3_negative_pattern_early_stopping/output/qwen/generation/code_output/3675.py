class Solution:
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        n = len(edges) + 1
        graph = [[] for _ in range(n)]
        total = 0
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
            total += w
        
        # We'll use a greedy approach: we want to keep edges with higher weights, but we have to ensure that no node has more than k edges.
        # We can think of it as: initially, we can keep all edges, but then we have to remove edges that cause some node to exceed k.
        # Alternatively, we can use a two-pass method: first, compute the current degree of each node (if we kept all edges, then each node's degree is the number of edges connected to it).
        # Then, we can use a max-heap to keep track of the edges that are causing the degree to exceed k.

        # But note: the problem is that removing one edge might help multiple nodes. Actually, we can use a different approach.

        # We can use a greedy algorithm that considers edges in descending order of weight. For each edge, we check if adding it (i.e., keeping it) would cause any node's degree to exceed k. But actually, we are allowed to remove edges arbitrarily, so we can choose which edges to keep.

        # However, the tree structure complicates things because edges are connected. But note: the condition is only on the degree, not on connectivity.

        # Actually, the problem is equivalent to: select a set of edges (from the tree) such that the degree of each node is at most k, and the sum of weights is maximized.

        # This is a well-known problem: the maximum spanning subgraph with degree constraints. In a tree, we can use a greedy method.

        # Steps:
        # 1. Calculate the current degree of each node (if all edges are kept).
        # 2. We need to remove edges until no node has degree > k. But we want to remove edges with the smallest weights first to maximize the remaining sum.

        # However, note: removing an edge affects two nodes. So, we can use a priority queue (min-heap) for edges by weight, and then for each node that has degree > k, we remove the edge with the smallest weight connected to it. But then, removing an edge might fix two nodes, but we have to update the degrees.

        # But wait, the problem is that we are allowed to remove edges arbitrarily, and we want to maximize the sum. So, we can keep as many edges as possible, but we cannot exceed k for any node.

        # Actually, the maximum number of edges we can keep is (n * k) // 2, but that's the maximum number, not the sum. We need to maximize the sum.

        # Another approach: sort the edges in descending order of weight. Then, for each edge, if adding it doesn't cause any node to exceed k, then add it. But in a tree, the edges are not independent in terms of connectivity, but the degree condition is local.

        # However, note: the tree is connected, but we are allowed to break it. The condition is only on the degree. So, we can consider each edge independently.

        # But the catch: if we keep an edge, it increases the degree of two nodes. So, we need to ensure that after keeping an edge, both nodes' degrees are <= k.

        # We can use a greedy algorithm that starts with no edges and adds edges in descending order, but that would be the same as keeping the highest weight edges as long as the degree condition is satisfied. But note: if we keep an edge, we must keep it for both nodes. 

        # Actually, the problem is equivalent to: select a set of edges (from the tree) such that the degree of each node is at most k, and the sum of weights is maximized.

        # This is a matroid intersection problem, but we can solve it greedily.

        # Steps for greedy:
        # 1. Sort edges by weight descending.
        # 2. Initialize an array for degrees (all zeros).
        # 3. For each edge (u, v, w) in descending order:
        #    - If degree[u] < k and degree[v] < k, then we can keep this edge. Then, increment degree[u] and degree[v] by 1, and add w to the result.
        #    - Otherwise, skip this edge (i.e., remove it).
        # 4. Return the result.

        # But wait, is that correct? Let's test with Example 1.

        # Example 1: edges = [[0,1,