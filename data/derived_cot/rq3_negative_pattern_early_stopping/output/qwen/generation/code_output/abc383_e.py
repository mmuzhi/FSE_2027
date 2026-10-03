import sys
import sys
sys.setrecursionlimit(300000)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it)); k = int(next(it))
    
    edges = []
    for _ in range(m):
        u = int(next(it)); v = int(next(it)); w = int(next(it))
        edges.append((u, v, w))
        
    A = [int(next(it)) for _ in range(k)]
    B = [int(next(it)) for _ in range(k)]
    
    # Build MST using Kruskal
    edges.sort(key=lambda x: x[2])
    parent = list(range(n+1))
    rank = [0]*(n+1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True

    mst_edges = []
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == n-1:
                break
                
    # Build graph from MST edges
    graph = [[] for _ in range(n+1)]
    for u, v, w in mst_edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
        
    # Precompute parent and depth for binary lifting for LCA
    depth = [0]*(n+1)
    parent_table = [[0]*(n+1) for _ in range(20)]
    # We'll do a BFS to set depth and parent0
    from collections import deque
    q = deque()
    q.append(1)
    depth[1] = 0
    parent_table[0][1] = 0
    while q:
        u = q.popleft()
        for v, w in graph[u]:
            if v == parent_table[0][u]:
                continue
            depth[v] = depth[u] + 1
            parent_table[0][v] = u
            q.append(v)
            
    # Build the binary lifting table
    for i in range(1, 20):
        for j in range(1, n+1):
            parent_table[i][j] = parent_table[i-1][parent_table[i-1][j]]
            
    # Function to compute LCA and the maximum edge weight on the path
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # Bring u up to the depth of v
        d = depth[u] - depth[v]
        max_edge = 0
        bit = 0
        while d:
            if d & 1:
                # Lift u and track the maximum edge
                # But we need to track the maximum edge on the path
                # We can store the maximum edge for each jump
                # Alternatively, we can do two passes: one for depth adjustment and then for LCA
                pass  # We'll refactor

    # Actually, we need to compute the bottleneck (max edge) between u and v.
    # We can do:
    #   Lift u and v to the same depth, tracking the maximum edge.
    #   Then lift both until their parents are the same, tracking the maximum edge.
    # But we need to store the maximum edge for each jump.

    # Let's modify the binary lifting to store the maximum edge for each jump.
    # We'll create a new table: max_edge_table[i][j] = the maximum edge weight on the path from j to its 2^i-th parent.
    max_edge_table = [[0]*(n+1) for _ in range(20)]
    
    # First, set the 0-th level (direct parent)