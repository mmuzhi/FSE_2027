import sys
from collections import deque

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it)); m = int(next(it)); k = int(next(it))
    edges = []
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        edges.append((u, v))
    
    # If k == 0, then we cannot flip any edge, so the shortest path is the original number of edges (which is the number of edges in the shortest path)
    # But note: the original graph has edges of weight 0, so the shortest path is the number of edges in the shortest path (counting edges, not weights).
    # However, the problem allows flipping exactly K edges. So if k==0, then we flip 0 edges, so the shortest path is the minimum number of edges (each weight 0) from 1 to N.
    # But the problem says: initially all edges weight 0, and we choose exactly K edges to change to 1.
    # So if k==0, then no edge is flipped, so the shortest path is the minimum number of edges (each weight 0) from 1 to N.
    # But the answer is the shortest path's weight, which is the number of edges in the path (since each edge is 0). 
    # However, the problem's sample input 3 3 2 has answer 1, which is not the number of edges (which is 1 for the direct edge, but the shortest path in terms of weight is 1 because the edge is flipped to 1).
    # Let me re-read the problem: 
    # "Initially, all edges have weight 0. We choose exactly K out of the M edges and change their weights to 1. Find the maximum possible value of the shortest distance from vertex 1 to vertex N in the resulting graph."
    # The shortest distance is the sum of weights. 
    # In the sample input 3 3 2, by choosing edges 1 and 3 (which are (1,2) and (1,3)), the shortest path from 1 to 3 is 1 (using the edge (1,3) which is flipped to 1). 
    # But note: the edge (1,3) is one edge, so the weight is 1.
    # In the original graph (without flipping), the shortest path from 1 to 3 is 1 (using the edge (1,3)) but with weight 0, so the distance is 0. 
    # But wait, the problem says "Initially, all edges have weight 0", so the shortest distance is 0 if there's a direct edge? 
    # But then, flipping the edge (1,3) to 1 makes the shortest distance 1.
    # So the answer is the maximum possible shortest distance (which is the minimum total weight) after flipping exactly K edges.
    # So, we want to maximize the minimum total weight from 1 to N.

    # Approach:
    # We can use a BFS that considers the graph and then we are allowed to "pay" 1 for each flipped edge. But we must flip exactly K edges.
    # However, note: we are allowed to flip any K edges, and the shortest path is the minimum total weight (number of flipped edges used) over all paths.
    # We want to maximize that minimum.

    # We can use a binary search on D (the answer). D can range from 0 to the maximum possible (which is the length of the longest path from 1 to N, but note we can only flip K edges, so D cannot exceed K).
    # But note: the minimum total weight cannot exceed K (because a path can have at most the number of edges in the path, but we can only have K flipped edges).

    # For a fixed D, we want to check if there exists a set S (size K) such that the shortest path (minimum total weight) from 1 to N is at least D.

    # But note: the shortest path is the minimum number of edges from S in any path. 
    # This is equivalent to: the minimum number of edges from S in any path is >= D.

    # How to check for a fixed D?
    # We can use a BFS that explores the graph and keeps track of the number of edges from S used so far. But we don't know S.

    # Alternatively, we can use a different idea: 
    # We want to know if there exists a set S (size K) such that every path from 1 to N has at least D edges from S.
    # This is equivalent to: the minimum number of edges from S in any path is >= D