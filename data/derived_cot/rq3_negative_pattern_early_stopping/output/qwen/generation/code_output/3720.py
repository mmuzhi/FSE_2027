class Solution:
    def minMaxWeight(self, n: int, edges: List[List[int]], threshold: int) -> int:
        # Build graph with edges and weights
        graph = [[] for _ in range(n)]
        for a, b, w in edges:
            graph[a].append((b, w))
        
        # We'll use binary search on the maximum edge weight
        # Conditions: For a candidate weight X, we can only keep edges with weight <= X.
        # Then, we need to check if from every node we can reach node 0, and also that each node has at most threshold outgoing edges (with weight <= X).
        # But note: the condition of having at most threshold outgoing edges must hold for the graph we keep.

        # However, note that the problem requires two things: 
        # 1. The graph must have node 0 reachable from all nodes.
        # 2. Each node has at most threshold outgoing edges.
        # And we want to minimize the maximum edge weight.

        # We can use binary search on the maximum edge weight. Let's define a function feasible(X) that returns True if there exists a graph with maximum edge weight <= X that satisfies the conditions.

        # Steps for feasible(X):
        # 1. Build a graph with only edges having weight <= X.
        # 2. For each node, count the number of outgoing edges (with weight <= X). If any node has more than threshold, then X is not feasible.
        # 3. Check if node 0 is reachable from all nodes. But note: the condition is that node 0 must be reachable from all other nodes. This means we need to check that from every node, there is a path to node 0.

        # However, note: the graph is directed. We need to check reachability from every node to node 0. We can do a BFS/DFS from node 0 and mark all nodes that can reach node 0? Actually, we need to check for each node if there's a path from that node to node 0. Alternatively, we can reverse the graph and then check from node 0 which nodes can reach it.

        # Actually, the condition is: Node 0 must be reachable from all other nodes. So, we need to check that every node (except 0) has a path to node 0. We can do:
        #   - Reverse the graph (edges reversed) and then do a BFS/DFS from node 0 to mark all nodes that can reach node 0 (in the original graph, these are the nodes that have a path to node 0). Then, check if all nodes are marked.

        # But note: the graph we build for the candidate X must be the same graph we use for reachability and counting outgoing edges.

        # However, the problem is that the graph is directed, and we are removing edges. We must ensure that in the graph with edges only <= X, the reachability condition holds and the threshold condition holds.

        # Steps for feasible(X):
        # 1. Build a graph (adjacency list) for edges with weight <= X.
        # 2. For each node, count the number of outgoing edges (in this graph). If any node (including node 0) has more than threshold, return False.
        # 3. Reverse the graph (for reachability: we want to know which nodes can reach node 0, so we reverse the edges and start from node 0 and do BFS/DFS to mark all nodes that can reach node 0 in the original graph). Then, check if all nodes are marked (i.e., every node has a path to node 0).

        # But wait: the graph we built in step 1 is the graph with edges <= X. The reachability condition must be checked on this graph. So, we need to check in the graph with edges <= X, if from every node there is a path to node 0.

        # Actually, we can do:
        #   - Build the graph for candidate X (edges with weight <= X).
        #   - Then, from node 0, do a BFS/DFS to mark all nodes reachable from node 0. But that's the opposite: we need to check that from every node, node 0 is reachable. 

        # Alternatively, we can reverse the graph (edges reversed) and then from node 0, mark all nodes that can reach node 0 (in the original graph). Then, check if all nodes are marked.

        # But note: the graph we built is for edges <= X. So, we can build the reversed graph for edges <= X and then do BFS from node 0 in the reversed graph to mark all nodes that can reach node 0 (in the original graph) using edges <= X.

        # However, note that the graph might have multiple edges, but the