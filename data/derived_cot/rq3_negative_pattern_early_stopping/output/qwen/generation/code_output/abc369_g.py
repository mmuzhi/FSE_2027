import sys
import heapq
from collections import defaultdict

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    n = int(data[0])
    graph = defaultdict(list)
    index = 1
    for _ in range(n-1):
        u = int(data[index]); v = int(data[index+1]); w = int(data[index+2])
        index += 3
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    # Precompute distances from node 1 to all nodes
    dist = [-1] * (n+1)
    parent = [0] * (n+1)
    depth = [0] * (n+1)
    stack = [1]
    dist[1] = 0
    while stack:
        node = stack.pop()
        for neighbor, weight in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + weight
                parent[neighbor] = node
                stack.append(neighbor)
    
    # Precompute LCA (binary lifting)
    LOG = (n).bit_length()
    up = [[0] * (n+1) for _ in range(LOG)]
    # up[0] is the parent array
    for i in range(1, n+1):
        up[0][i] = parent[i]
    
    for i in range(1, LOG):
        for node in range(1, n+1):
            if up[i-1][node] != 0:
                up[i][node] = up[i-1][up[i-1][node]]
            else:
                up[i][node] = 0
    
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # Bring a up to the same depth as b
        d = depth[a] - depth[b]
        bit = 0
        while d:
            if d & 1:
                a = up[bit][a]
            d //= 2
            bit += 1
        
        if a == b:
            return a
        
        for i in range(LOG-1, -1, -1):
            if up[i][a] != up[i][b]:
                a = up[i][a]
                b = up[i][b]
        return up[0][a]
    
    # Precompute the distance between any two nodes
    def distance(u, v):
        w = 0
        u0, v0 = u, v
        while u != v:
            if depth[u] > depth[v]:
                w += dist[u] - dist[lca(u, v)]
                u = parent[u]
            elif depth[v] > depth[u]:
                w += dist[v] - dist[lca(u, v)]
                v = parent[v]
            else:
                w += dist[u] - dist[lca(u, v)] + dist[v] - dist[lca(u, v)]
                break
        return w
    
    # But note: the above distance function is not efficient and might be incorrect.

    # Alternatively, we can use the fact that dist[u] + dist[v] - 2 * dist[lca(u, v)] is the distance between u and v.
    # Let's define a better distance function.
    def node_distance(u, v):
        wu = dist[u]
        wv = dist[v]
        w = dist[u] + dist[v] - 2 * dist[lca(u, v)]
        return w
    
    # Now, the minimal walk for a set S is not simply twice the sum of distances from 1, but we need to find the minimal way to cover S and return to 1.

    # However, after reading sample solutions for similar problems, I recall that the minimal walk is the sum of the distances from 1 to each vertex in S, multiplied by 2, minus the savings from the fact that the paths overlap.

    # But actually, the minimal walk is the same as the minimal Steiner Tree for T = S ∪ {1} multiplied by 2. But the Steiner Tree for T is the minimal tree connecting T, and its length is the sum of the distances from 1 to each vertex in S, minus the savings from the shared edges.

    # But there's a known result: the minimal walk is 2 * (sum_{v in S} dist[v]) - 2 * (sum_{v in S} dist[lca(v, 1)]) but that doesn't make sense.

    # Let me think differently.

    # The minimal walk must cover all vertices in S and return to 1. The minimal way is to use the following: the walk must go from 1 to each vertex in S and back