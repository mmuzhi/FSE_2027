import heapq
import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    edges = []
    for _ in range(m):
        a = int(next(it)) - 1; b = int(next(it)) - 1; c = int(next(it))
        edges.append((a, b, c))
    
    # Build graph for Dijkstra from node 0 (city 1) and node n-1 (city N)
    graph = [[] for _ in range(n)]
    for a, b, c in edges:
        graph[a].append((b, c))
        graph[b].append((a, c))
    
    # Dijkstra from node 0 (city 1)
    d1 = [10**18] * n
    d1[0] = 0
    heap = [(0, 0)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist != d1[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < d1[neighbor]:
                d1[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
                
    # Dijkstra from node n-1 (city N)
    d2 = [10**18] * n
    d2[n-1] = 0
    heap = [(0, n-1)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist != d2[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < d2[neighbor]:
                d2[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
                
    base = d1[n-1]
    # If base is still 10**18, then there's no path? But the problem states that with all roads, city N is reachable.
    # So base should be finite.
    
    # Now, for each edge, we check:
    #   Let candidate = min(d1[u] + w + d2[v], d1[v] + w + d2[u])
    #   If candidate > base, then the edge is not used in any shortest path -> removing it doesn't change the base -> output "No"
    #   Else, we need to check if there is an alternative path of length base that does not use the edge.
    #
    # But note: the entire base might be achieved by multiple paths. We need to check if the edge is the only way to achieve base.
    #
    # Actually, we can use the following: 
    #   The edge is critical if and only if:
    #       candidate == base   (i.e., the edge is part of a shortest path) AND
    #       (d1[u] + w + d2[v] == base OR d1[v] + w + d2[u] == base)   [which is already satisfied by candidate==base] 
    #       AND
    #       There is no other path (not necessarily using the edge) that achieves base? 
    #
    # But note: the base is fixed. The condition for the edge to be critical is that the edge is the only way to achieve base? Not exactly.
    #
    # Actually, the edge is critical if and only if the shortest path without the edge is greater than base.
    #
    # However, we cannot compute the shortest path without the edge easily.
    #
    # Alternate known solution: 
    #   We can use the following: 
    #       Let base = d1[n-1]
    #       For each edge (u, v, w):
    #           candidate = min(d1[u] + w + d2[v], d1[v] + w + d2[u])
    #           if candidate > base:
    #               print("No")
    #           else:
    #               # Check if the edge is the only way to achieve base: 
    #               #   But note: there might be multiple edges that are part of the shortest path. 
    #               #   Actually, we can check: 
    #               #       Let base_alt = base   (if there is an alternative path of length base that doesn't use the edge)
    #               #   How? We can check: 
    #               #       The shortest path without the edge is base if there exists a path from 1 to N of length base that does not use the edge.
    #               #   But note: the entire graph without the edge: we don't know.
    #