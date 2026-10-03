import heapq
import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it)); q = int(next(it))
    
    # Read edges
    edges = []
    graph = [[] for _ in range(n+1)]
    for i in range(m):
        a = int(next(it)); b = int(next(it)); c = int(next(it))
        edges.append((a, b, c))
        graph[a].append((b, c, i+1))
        graph[b].append((a, c, i+1))
    
    # We'll maintain a set (or list) of removed edges (by index)
    removed_edges = set()
    # We'll store the queries
    queries = []
    for i in range(q):
        t = next(it)
        if t == '1':
            i_val = int(next(it))
            queries.append(('close', i_val))
        else:  # t == '2'
            x = int(next(it)); y = int(next(it))
            queries.append(('query', x, y))
    
    # We'll process the queries and for each query of type 2, run Dijkstra on the graph excluding removed_edges
    # But we cannot run Dijkstra 200000 times because it's too slow.
    # Instead, we use the fact that the number of removals is at most 300, so we can rebuild the graph from scratch for each query 2, but that is too slow.

    # Alternative: use the original graph and skip removed edges during Dijkstra. But worst-case 200000 * (number of edges) is too slow.

    # We need a better idea.

    # Since the graph is small (n=300) and the removals are few (at most 300), we can use the following:
    # Precompute the original graph's APSP (all-pairs shortest paths) and then update the distances when edges are removed.
    # But updating APSP for edge removals is non-trivial.

    # However, note: the queries are online. We can use a "dynamic" APSP that updates for each removal. But there is a simpler idea:

    # We can store the original graph and then for each query 2, we run a Dijkstra that uses the original graph but skips edges that are removed.
    # But the number of edges is large (45000) and the number of queries is large (200000) so we need to optimize.

    # We can use a technique: since the graph is small (300 nodes) and the removals are few, we can use the following:
    #   Precompute the original graph's APSP (Floyd-Warshall) and store a 2D array dist[u][v] for the original graph.
    #   Then, when an edge is removed, we update the APSP for all pairs that are affected by that edge removal. But updating Floyd-Warshall for one edge removal is O(n^2) per removal, and we have 300 removals, so total 300 * n^2 = 300 * 90000 = 27e6, which is acceptable.

    # But then, how to update the APSP when an edge is removed? We can do:

    #   Let the removed edge be (u, v, weight). Then, we set the direct edge between u and v to infinity (or removed) and then run Floyd-Warshall again? But that would be O(n^3) per removal, so 300 * 300^3 = 300 * 27e6 = 8.1e9, which is acceptable in C++ but in Python might be borderline.

    # However, we have to update the graph and then answer queries. We can do:

    #   Precompute the initial APSP (Floyd-Warshall) for the original graph.
    #   Then, for each removal, update the APSP by setting the edge to infinity and then running Floyd-Warshall again? But that would be too slow.

    # Actually, we can update the APSP without rerunning the entire Floyd-Warshall. We can use the following:

    #   Let G be the graph (adjacency matrix) with direct edge weights. Initially, we set G[i][j] to the weight of the edge (i, j) if exists, else a large number (inf).
    #   Then, the APSP is computed by:
    #       for k in range(1, n+1):
    #           for i in range(1, n+1):
    #               for j in range(1, n