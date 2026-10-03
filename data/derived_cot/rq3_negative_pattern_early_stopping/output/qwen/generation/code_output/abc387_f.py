import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # Build the graph (0-indexed)
    graph = [[] for _ in range(n)]
    for i in range(n):
        # A[i] is given, but note: the input A_i is between 1 and N, so we subtract 1 to make 0-indexed.
        graph[i].append(A[i]-1)
    
    # We'll use a visited array for cycle detection and also to mark nodes that are part of a cycle.
    visited = [False] * n
    in_cycle = [False] * n
    cycle_nodes = set()
    
    # We'll do a DFS or use a two-pass method to detect cycles in a functional graph.
    # Alternatively, we can use a topological sort (Kahn's algorithm) to remove nodes that are not in cycles.
    # But since each node has one outgoing edge, we can use a method of following the chain until we find a cycle.
    
    # We'll use a visited marker and a recursion stack, but n is up to 2025, so recursion might be deep. Alternatively, we can use iterative DFS or a two-pointer (Floyd's cycle finding) for each node? But that might be too slow.
    
    # Instead, we can use a method: for each node, we can traverse until we find a node that is visited. But we need to mark cycles.
    
    # Alternatively, we can use a visited array and a current path array, but again, we have to be careful.
    
    # Let's use a method: for each node, we can follow the chain and mark nodes until we find a node that is either visited or in the current path.
    
    # But we can also use the following: 
    #   Step 1: Compute the in-degree for each node (for the graph, but note: each node has one outgoing edge, so in-degree can be more than one).
    #   Step 2: Use a queue to remove nodes with in-degree 0. Then the remaining nodes are in cycles.
    
    # Actually, that's a standard way to find cycles in a functional graph.
    
    in_degree = [0] * n
    for i in range(n):
        neighbor = graph[i][0]
        in_degree[neighbor] += 1
    
    q = deque()
    for i in range(n):
        if in_degree[i] == 0:
            q.append(i)
    
    # Remove nodes with in_degree 0
    while q:
        node = q.popleft()
        visited[node] = True
        next_node = graph[node][0]
        in_degree[next_node] -= 1
        if in_degree[next_node] == 0:
            q.append(next_node)
    
    # Now, the remaining nodes are in cycles.
    for i in range(n):
        if not visited[i]:
            in_cycle[i] = True
            # Mark all nodes in the cycle
            cur = i
            while not visited[cur]:
                visited[cur] = True
                in_cycle[cur] = True
                cur = graph[cur][0]
    
    # Now, we need to compute the answer.
    # The idea: the nodes in the cycle must have the same value. Let that value be c (from 1 to M). Then, for each node not in the cycle, the value must be ≤ the value of the node it points to (which is closer to the cycle). And the entire chain must be non-decreasing? Actually, the condition is only direct edges, but by transitivity, the entire chain must be non-decreasing. However, note that the condition is only for direct edges, but the constraints are independent for each edge. However, the condition for a node u is x_u ≤ x_{A_u}. And if A_u is in the cycle, then x_u ≤ c. But also, if u points to a node v that is not in the cycle, then x_u ≤ x_v, and so on until the cycle.
    
    # Actually, the constraints form a partial order: the value at a node must be ≤ the value at the node it points to, and by transitivity, ≤ all nodes reachable from it. But note: the graph is a functional graph, so from a node, there is exactly one path. So, the constraints are: for each node u, x_u ≤ x_{next(u)} ≤ x_{next(next(u))} ≤ ... ≤ x_{cycle_node}.
    
    # Therefore, the value at u must be ≤ the value at the cycle node it eventually reaches. And the cycle node