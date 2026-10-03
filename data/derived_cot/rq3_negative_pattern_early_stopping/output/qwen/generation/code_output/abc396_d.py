import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    graph = [[] for _ in range(n+1)]
    
    for _ in range(m):
        u = int(next(it)); v = int(next(it)); w = int(next(it))
        graph[u].append((v, w))
        graph[v].append((u, w))
        
    # We'll use BFS with state (current node, visited set) but that is too heavy because the set can be represented as a bitmask (n<=10, so 10 bits) and we can use DP with bitmask and node.
    # Alternatively, we can do DFS with memoization: dp[node][mask] = minimum XOR value from node 1 to node (node) with visited mask (mask). But note: we are not storing the entire path, but the XOR value. However, the same node and mask can be reached by different XOR values, and we want the minimum XOR value for that state? But note: the XOR operation is not linear and we cannot simply take the minimum because the path might be extended differently.

    # Actually, we can use the following: we want to compute the minimum XOR from 1 to N. We can use a dictionary for each node: best[node][mask] = the minimum XOR value that reaches node with the set of visited nodes (mask). But note: the XOR value is not necessarily additive in the sense of state, but we are combining edges.

    # However, the state space is 10 * 2^10 = 10240 states. We can do a BFS or DFS that goes through each state (node, mask) and stores the minimum XOR value for that state.

    # Steps:
    # 1. Start from node 1 with mask = 1 << 0 (if nodes are 1-indexed, then mask for node 1 is 1) and XOR value 0.
    # 2. For each neighbor, if not visited, update the mask and the XOR value (current XOR ^ edge_weight).
    # 3. We want to reach node N (node index n) with any mask.

    # But note: the graph is undirected and we are only allowed to visit each node once.

    # However, the problem: the XOR operation is not reversible and we are not storing the entire path. But we are storing the XOR value so far. We cannot simply store the minimum XOR value for a state because the same state (node, mask) might be reached by different paths with different XOR values, and we want the minimum one.

    # We can do:
    #   dp[node][mask] = minimum XOR value to reach node with the set of visited nodes (mask) OR we can store a dictionary for each node: for a given mask, the minimum XOR value that achieves that state.

    # But note: the XOR value is not necessarily the same for the same mask and node. However, if we reach the same node with the same mask by two different paths, then the XOR value is fixed for that path? Actually, no: the XOR value depends on the edges taken. But the mask is the set of visited nodes, and the XOR value is the cumulative XOR of the edges. We are not storing the entire path, but the XOR value is the result of the edges.

    # We can use a DP table: dp[mask][node] = minimum XOR value to reach node with the set of visited nodes (mask). But note: the XOR operation is not linear and we cannot combine states arbitrarily. However, we can update the state by traversing edges.

    # Steps for DP:
    #   Let dp[mask][node] = minimum XOR value to reach node with the set of visited nodes (mask). We initialize dp[1<<0][1] = 0.
    #   Then, for each state (mask, node) and for each neighbor (v, weight) of node:
    #       if v is not in mask, then new_mask = mask | (1<<(v-1))
    #       new_xor = dp[mask][node] ^ weight
    #       Then, if we haven't seen (new_mask, v) or if we have seen it with a larger XOR value, update dp[new_mask][v] = new_xor.

    #   Then, we look at all states that reach node n (node index n) and take the minimum XOR value.

    # But note: the graph is undirected and we are allowed to traverse edges in any direction. We are building the path from 1 to n.

    # However, the state space is 2^10 * 10 = 10240 states, which is acceptable.

    # But