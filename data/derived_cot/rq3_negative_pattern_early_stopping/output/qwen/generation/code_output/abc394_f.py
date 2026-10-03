import sys
from collections import deque, defaultdict

sys.setrecursionlimit(300000)

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    edges = []
    index = 1
    graph = [[] for _ in range(n+1)]
    for i in range(n-1):
        a = int(data[index]); b = int(data[index+1]); index += 2
        edges.append((a, b))
        graph[a].append(b)
        graph[b].append(a)
    
    parent = [0] * (n+1)
    depth = [0] * (n+1)
    order = []
    stack = [1]
    parent[1] = 0
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            stack.append(neighbor)
    
    # Build Euler Tour order for LCA queries? Or use binary lifting? Actually, we might need to do DP on trees.
    # Alternatively, we can do a DFS to compute the tree structure.

    # We'll do a DFS to compute the tree structure and then use DP.

    # Let dp[u][state] be the maximum alkane subgraph in the subtree rooted at u, where state indicates the number of edges used from u to its parent (if any) and the number of children edges used.

    # But note: the alkane condition is on the entire subgraph. We need to consider the degrees.

    # Alternatively, we can think: the alkane is a tree where each node has degree 1 or 4. So, we can model the problem as: we want to select a connected subgraph (a tree) such that each node has degree 1 or 4.

    # We can use a DP that considers the node and the number of edges we have used from this node (to parent and children). But note: the node can have at most 4 edges.

    # Let's define:
    # dp[u][k] = the maximum number of vertices in the alkane subgraph rooted at u, given that u has k edges (k can be 0, 1, 2, 3, 4) already used (from parent and children). But wait, the node u can have at most 4 edges. The state k would be the number of edges incident to u that are part of the alkane.

    # However, the alkane condition requires that the node must have degree 1 or 4. So, at the end, k must be 1 or 4.

    # But during the DP, we can have intermediate states.

    # Steps:
    # 1. Root the tree arbitrarily (say at node 1).
    # 2. Do a DFS to compute the DP for each node.

    # The DP state: dp[u][k] = maximum number of vertices in the alkane subgraph rooted at u, with u having k edges (k from 0 to 4) already connected (to parent and children). But note: the parent edge is not known until we do a second pass (like a reroot DP). Alternatively, we can do a DFS that considers the parent's edge.

    # Actually, we can do a DP that considers the node and the number of children edges we use, and then the parent edge is separate.

    # Alternatively, we can use a state that includes the number of edges used from the parent and the number of edges used from the children.

    # Let's define:
    # dp[u][a][b] = maximum alkane subgraph in the subtree rooted at u, where a is the number of edges from u to its parent (0 or 1) and b is the number of edges from u to its children (0 to 4). But then the total edges at u is a + b, and we require that at the end, a + b is 1 or 4.

    # But the state space is 2 * 5 = 10 states per node, and we have 200,000 nodes, so 2e6 states, which is acceptable.

    # However, we need to consider that the parent edge is only one, and the children edges are multiple.

    # Steps for DP:

    # 1. Root the tree at node 1.
    # 2. For each node u, we consider the edges to its children (excluding the parent). Then, we can choose to use some of these edges (but the alkane condition must hold for u).

    # But note: the alkane condition must hold for every node in the subgraph. So, when we build the subgraph,