import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    k = int(data[1])
    edges = []
    index = 2
    for i in range(n-1):
        a = int(data[index]); b = int(data[index+1]); index += 2
        edges.append((a, b))
    
    required = list(map(int, data[index:index+k]))
    index += k

    # Build the tree as an adjacency list
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    # We are going to use the idea: the minimal connected subgraph containing the required vertices is the union of the simple paths between the required vertices.
    # But note: we can also think of it as the minimal Steiner Tree in a tree. However, we can use the following method:

    # Step 1: Mark the required vertices.
    # Step 2: We can use the concept of "virtual tree" or "centroid" but note constraints (up to 200000) so we need an efficient method.

    # Alternate approach: 
    #   We can use the following observation: the minimal connected subgraph is the union of the simple paths between the required vertices. 
    #   But note: the minimal connected subgraph is the minimal subtree that contains all the required vertices.

    # How to compute the minimal subtree? 
    #   We can do: 
    #   1. Find the diameter of the set of required vertices? Actually, we can use the following:
    #   2. The minimal subtree is the union of the simple paths between the required vertices. But note, we can also use the following method:

    #   We can use the following algorithm:
    #   - Let T be the set of required vertices.
    #   - We can compute the minimal Steiner Tree by first building a "virtual tree" of the required vertices. But note, the problem is in a tree.

    #   However, note: the minimal Steiner Tree in a tree is the union of the simple paths between the required vertices, and the number of vertices is the number of distinct vertices in that union.

    #   But how to compute the union of the simple paths between all pairs? That would be too expensive.

    #   Alternate known method: 
    #   - We can use the fact that the minimal connected subgraph containing T is the union of the simple paths between the vertices in T. 
    #   - We can use the following: 
    #       Let L be the set of leaves (required vertices) of the Steiner tree. Then the Steiner tree is the minimal subtree that contains all the required vertices.

    #   Steps:
    #   1. We can use the following: 
    #       a. Find the set of required vertices.
    #       b. We can use the idea of "least common ancestors" (LCA) to compute the union of paths.

    #   However, note: the minimal Steiner Tree in a tree is also known as the minimal subtree spanning the set T.

    #   We can compute the minimal subtree by:
    #       - Start with the entire set T.
    #       - Then, repeatedly remove leaves that are not in T until only the internal nodes (which are in the Steiner tree) remain? But that is not efficient.

    #   Another known method: 
    #       - The minimal Steiner Tree in a tree can be found by:
    #           * Find the set of required vertices.
    #           * Compute the set of "Steiner points" (which are the vertices that are not required but must be included to connect the required vertices).
    #       - Actually, the minimal Steiner Tree is the union of the simple paths between the required vertices. The number of vertices is the number of distinct vertices in the union.

    #   But note: we can use the following efficient method:

    #   Step 1: Mark the required vertices.
    #   Step 2: Use a BFS/DFS to compute the distance between required vertices? But that is too heavy.

    #   Alternatively, we can use the following trick:

    #   We can use the concept of "virtual tree" (also called the minimal Steiner tree in trees) by:
    #       1. Build a tree that only contains the required vertices and the necessary Steiner points (which are the LCA of pairs of required vertices). But building the virtual tree is O(K log K).

    #   Steps for building the virtual tree (Steiner tree in a tree):
    #       a. For each required vertex, mark it.
    #       b. For each required vertex, we