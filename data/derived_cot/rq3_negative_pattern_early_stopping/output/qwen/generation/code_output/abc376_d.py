import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    graph = [[] for _ in range(n+1)]
    for _ in range(m):
        a = int(next(it)); b = int(next(it))
        graph[a].append(b)
    
    # If there's a self-loop at vertex 1, then cycle length is 1.
    if 1 in graph[1]:
        print(1)
        return

    # We'll do a BFS starting from vertex 1, but we need to record the distance from 1 to each node.
    # However, we are looking for a cycle, so we need to find a path from a neighbor of 1 back to 1.
    # We can use the following: remove vertex 1 and then find the shortest path from each neighbor of 1 to 1, but that doesn't work because the graph is directed.

    # Alternatively, we can use BFS from all neighbors of 1 simultaneously, but then we need to avoid going back to 1 until we have a cycle.

    # Actually, we can use the following method:
    # Let's consider the graph without vertex 1. Then, for each edge from 1 to u, we look for the shortest path from u to 1 in the original graph, but without using the edge from 1 to u? Not exactly.

    # Another idea: use BFS from vertex 1, but when we encounter a node that is already visited (but not necessarily from the same BFS), then we can compute the cycle length.

    # But that might not work because the graph is large.

    # Standard approach for shortest cycle containing a vertex in a directed graph is to use BFS/DFS and then use the distance from the vertex to itself via other nodes.

    # Actually, we can do:
    # Let dist[u] be the shortest distance from vertex 1 to u (without using the cycle).
    # Then, for each edge (u, 1), the cycle length would be dist[u] + 1.
    # But wait, that's not necessarily the shortest cycle because the path from 1 to u might not be the direct one.

    # Alternatively, we can use the following:
    # 1. Do a BFS/DFS from vertex 1 to compute the shortest path to all nodes (without considering cycles).
    # 2. Then, for each node u that has an edge to 1, the cycle length is dist[u] + 1.
    # 3. Then, the answer is the minimum of these cycle lengths.

    # But wait, is that correct? Let's test with sample input 1:
    # 3 3
    # 1 2
    # 2 3
    # 3 1
    # 
    # dist[1] = 0, dist[2] = 1, dist[3] = 2.
    # Then, for u=3, cycle length = 2 + 1 = 3. Correct.
    # For sample input 3:
    # 6 9
    # 6 1
    # 1 5
    # 2 6
    # 2 1
    # 3 6
    # 4 2
    # 6 4
    # 3 5
    # 5 4
    # 
    # We need to compute dist from 1 to each node, then for each node u that has an edge to 1, compute dist[u] + 1 and take the minimum.

    # But wait, in sample input 3, the answer is 4. Let's see: 
    # The cycle is 1->2->6->4->2? No, that doesn't end at 1. Actually, the sample output is 4, so the cycle must be 1->2->6->4->5->1? Wait, no, that's 5 edges. Or maybe 1->2->6->4->2->1? But that's 5 edges too.

    # Wait, let me recheck sample input 3. The sample input 3 is:
    # 6 9
    # 6 1
    # 1 5
    # 2 6
    # 2 1
    # 3 6
    # 4 2
    # 6 4
    # 3 5
    # 5 4

    # The cycle that contains vertex 1 and has 4 edges: 
    # 1->2->6->4->5->1? That's 5 edges. Or 1->2->6->4->2