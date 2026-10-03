import sys
from collections import defaultdict, deque
import heapq

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    bridges = []
    for _ in range(m):
        u = int(next(it)); v = int(next(it)); t = int(next(it))
        bridges.append((u, v, t))
    
    # Build graph for the entire set of bridges
    graph = defaultdict(list)
    for u, v, t in bridges:
        graph[u].append((v, t))
        graph[v].append((u, t))
    
    # Precompute all pairs shortest paths? But N is 400, so Floyd-Warshall would be O(N^3) which is 64e6, acceptable in Pyton if optimized, but maybe we can do better.
    # Alternatively, we can use Dijkstra from each node? But that would be O(N*M*log(N)) which is 400 * 200000 * log(400) ~ 400 * 200000 * 9 = 720e6, which might be too slow in Python.
    # But note: the graph is undirected and we have up to 200,000 edges. We can use Floyd-Warshall for N=400 (which is 400^3 = 64e6) which is acceptable in C++ but in Python might be borderline. However, we can try to use Dijkstra from each node but only for the nodes that are relevant? Or use the fact that we have to use specific bridges.

    # Actually, the problem requires handling queries with up to 5 bridges. So, we can precompute the shortest path between all pairs of islands (nodes) because N is 400. Floyd-Warshall is O(N^3) which is 64e6, which is acceptable in Pyton if we use a 2D list and optimize with pypy or in C++ but in Python we might need to use a list of lists and hope that the input isn't worst-case.

    # But wait, the graph is undirected and we have multiple edges between same nodes? The problem says: "it is possible for two islands to be directly connected by more than one bridge." So, we need to consider the minimum edge between two nodes? Actually, no: because we are allowed to use any bridge, but the bridges are distinct. However, for the purpose of shortest path, we can take the minimum edge between two nodes? But note: the query requires using specific bridges. So, we cannot ignore the specific bridges.

    # Actually, the problem is: we must use each of the given bridges at least once. So, the path must include each of the specified bridges. We can use other bridges as well.

    # This is similar to the "Steiner path" problem with required edges. But Steiner path is NP-hard in general, but here the number of required edges is at most 5. So, we can consider the following:

    # Let the required bridges be a set S (size at most 5). We must use each bridge in S at least once. We can use other bridges arbitrarily.

    # We can think of the problem as: we have to traverse each bridge in S at least once. The order of traversal is arbitrary, and we can go in any direction.

    # This is similar to the Traveling Salesman Problem on the set of bridges, but we also have to connect from 1 to N.

    # Alternatively, we can consider the following: the entire journey must cover the set S. We can break the journey into segments that connect the endpoints of the bridges. But note, the bridges are edges, so each bridge has two endpoints.

    # Steps:

    # 1. Precompute the shortest path between every pair of islands (nodes) because N is 400. We can use Floyd-Warshall or Dijkstra from each node. Since the graph is undirected and we have up to 200,000 edges, Dijkstra from each node might be too slow (400 * (time for Dijkstra)). But 400 * (number of edges) * log(number of nodes) = 400 * 200000 * log(400) ~ 400 * 200000 * 9 = 720e6 operations, which is too slow in Python.

    # 2. Use Floyd-Warshall: O(N^3) = 400^3 = 64e6, which is acceptable in C++ but in Python might be borderline. However, we can try to use Floyd-Warshall.

    #