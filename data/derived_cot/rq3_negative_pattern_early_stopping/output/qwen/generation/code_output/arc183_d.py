import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    edges = []
    index = 1
    graph = [[] for _ in range(n+1)]
    for i in range(n-1):
        a = int(data[index]); b = int(data[index+1]); index += 2
        edges.append((a, b))
        graph[a].append(b)
        graph[b].append(a)
    
    # We are going to use a BFS to compute the diameter of the tree? Or maybe we need to find the matching.

    # But note: the problem says that the tree has a perfect matching (the edges (1,2), (3,4), ... (N-1, N) are present). But the tree might have more edges.

    # However, the removal condition: after removing two leaves, the remaining graph must have a perfect matching.

    # Observation: The entire tree is a tree and has a perfect matching. The removal of two leaves (which are matched in the matching) might break the matching, but we can form a new matching.

    # But note: the matching edges are fixed by the input? Actually, the input edges are given arbitrarily, but the condition is that the edges (1,2), (3,4), ... are present.

    # However, the problem does not specify that the matching is only these edges. It says the tree has a perfect matching. So the matching might be different.

    # But the problem says: "Specifically, for each i (1 ≤ i ≤ N/2), it is guaranteed that A_i=i×2-1 and B_i=i×2." So the edges (1,2), (3,4), ... are present, but the matching might use these edges or not.

    # Actually, the problem does not specify the matching. It just says the tree has a perfect matching.

    # So we are free to choose any matching as long as the graph has one.

    # But the removal condition is that after removal, the remaining graph must have a perfect matching.

    # How to solve?

    # Another idea: the problem is equivalent to decomposing the tree into N/2 edges (the matching) and then the removals are pairs of leaves. But wait, no.

    # Alternatively, note that the entire tree is a tree and has a perfect matching. The removal of two leaves must leave a graph with a perfect matching. This is similar to the concept of a matching-covered graph.

    # But I recall that in a tree, a perfect matching exists if and only if the number of vertices is even and the tree is "nice" in some way? Actually, any tree with even number of vertices does not necessarily have a perfect matching. But the problem states that it does.

    # Given the constraints, we need to output a sequence of N/2 pairs (each pair being two leaves) such that after each removal, the remaining graph has a perfect matching.

    # How to maximize the total score? The score is the sum of the distances between the two leaves in each operation.

    # The maximum distance between two leaves is the diameter of the tree. But we cannot necessarily take the diameter first because after removal, the graph might not have a perfect matching.

    # Another idea: consider that the entire tree can be decomposed into a set of paths or chains. But it's a tree.

    # Alternatively, we can use the following greedy approach:

    # 1. Find all leaves (degree 1 vertices).
    # 2. In each operation, choose two leaves that are as far apart as possible (maximize the distance) and remove them, and then update the graph.

    # But wait, is that always possible? We must ensure that after removal, the remaining graph has a perfect matching.

    # However, the problem says "Show one procedure that maximizes the total score." So if we can prove that by always choosing the two leaves with the maximum distance, we maintain the perfect matching condition, then that would be a solution.

    # But is that true? Let's test with the sample.

    # Sample 1: vertices 1,2,3,4. Leaves are 1 and 4. The distance is 3. Then remove them, then leaves are 2 and 3 (distance 1). So total 4.

    # Sample 2: vertices 1 to 8. Leaves are 4,6,8 initially. The maximum distance between two leaves: 
    #   4 to 8: 4-3-2-1-7-8: 5 edges.
    #   4 to 6: 4-3-2-1-5-6: 5 edges.
    #   6 to 8: 6-5-1-7-8: