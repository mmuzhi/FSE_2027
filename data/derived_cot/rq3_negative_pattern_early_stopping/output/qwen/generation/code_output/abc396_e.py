import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    conditions = []
    for _ in range(m):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        conditions.append((x, y, z))
    
    # If there are no conditions, then we can set all A_i to 0, which minimizes the sum.
    if m == 0:
        print(" ".join(["0"] * n))
        return

    # We'll consider up to 32 bits because Z_i up to 10^9 (which is < 2^30)
    max_bits = 31

    # Build a graph of conditions. Each condition (x, y, z) gives an equation for each bit.
    # But we can also think in terms of constraints on variables (nodes) and equations (edges).
    # We'll build an undirected graph where each node is an index from 1 to n.
    graph = defaultdict(list)
    # Also, we need to track the constraints for each node for each bit.
    # Alternatively, we can use a union-find or DFS for each bit? But the system is linear in GF(2) for each bit.

    # Actually, we can model the problem as: for each bit j, we have a graph where edges are the conditions that involve that bit.
    # But note: a condition (x, y, z) affects bit j only if the j-th bit of z is 1. If it's 0, then the equation is a_x_j == a_y_j; if 1, then a_x_j != a_y_j.

    # However, we can also use a different approach: for each node, we can set a base value and then propagate constraints.

    # Another idea: use a union-find for each bit? But the constraints are not necessarily connected.

    # Alternatively, we can use a two-coloring for each connected component in the graph built by the conditions (ignoring the bit) but then combine the bits.

    # But note: the graph is built from conditions, and each condition is an edge between two nodes. However, the same condition applies to all bits? Actually, no: each condition applies to all bits, but we break it into bits.

    # Actually, we can solve each bit independently. For each bit j, we build a graph with n nodes and edges for each condition where the j-th bit of Z is 1 (which gives an equation a_x_j ^ a_y_j = 1) and for those with 0, we have a_x_j ^ a_y_j = 0.

    # Then, for each bit j, we can traverse the graph and assign values (0 or 1) to each node such that the equations are satisfied.

    # But note: the graph might have multiple connected components. In each connected component, we can assign two possible colorings (like bipartite graph). However, the equation for a bit j is:
    #   If the edge has weight 0 (same bit), then the two nodes must have the same value.
    #   If the edge has weight 1 (different bit), then the two nodes must have different values.

    # So, for each bit j, we can build a graph and then do a BFS/DFS to assign 0/1 to each node, and check for consistency.

    # However, we have to do this for each bit from 0 to 30 (31 bits). And the graph for each bit is built from the conditions that have the j-th bit set in Z.

    # But note: the graph for each bit is the same set of nodes (n nodes) but only edges where the condition's Z has the j-th bit set to 1 or 0. Actually, we can precompute for each condition and each bit whether it's an equality (0) or inequality (1) for that bit.

    # But wait, the condition (x, y, z) for bit j: 
    #   Let z_bit = (z >> j) & 1
    #   Then the equation is: a_x_j ^ a_y_j = z_bit.

    # So, for each condition, for each bit j, we can add an edge between x and y with weight z_bit.

    # Then, for each bit j, we build a graph with n nodes and edges from conditions that have the j-th bit set in Z (and also conditions with 0? Actually, we need to consider all conditions for each bit? But wait, if a condition has a Z_i with j-th bit 0, then we require a_x_j == a_y_j, and if