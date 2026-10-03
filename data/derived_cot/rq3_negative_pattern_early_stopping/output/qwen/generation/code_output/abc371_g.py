import math
from math import gcd
from collections import defaultdict, deque

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    # Read permutation P (1-indexed) and convert to 0-indexed
    # Next n integers for P
    P = list(map(int, data[1:1+n]))
    # Next n integers for A
    A = list(map(int, data[1+n:1+2*n]))
    
    # Convert P to 0-indexed
    P0 = [x-1 for x in P]
    
    # Build graph for cycles
    visited = [False] * n
    cycles = []
    for i in range(n):
        if not visited[i]:
            cycle = []
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = P0[cur]
            cycles.append(cycle)
    
    # We'll create an array for the initial values in each cycle, but we need to know the order in the cycle.
    # Actually, we need to know for each index, the cycle it belongs to and its position in the cycle.
    cycle_index = [-1] * n
    for idx, cycle in enumerate(cycles):
        for j, node in enumerate(cycle):
            cycle_index[node] = (idx, j)
    
    # For each cycle, we have a list of the initial values (from A) at the nodes in the cycle, in the order of the cycle.
    # But note: the cycle we built is by following P0. The cycle is: [i0, i1, i2, ...] where i1 = P0[i0], i2 = P0[i1], etc.
    # Then the transformation by k: the value at node i_j is the value from the initial array at the node i_{(j+k) mod m} (if we consider the cycle as starting at i0, then the node at position (j+k) mod m is the node we land on after k steps from i_j).
    # But note: the operation is defined as: A^{(k)}[i] = A^{(0)}[P0^k(i)]
    # And P0^k(i) is the node we get by applying P0 k times to i.

    # However, we have the cycle, so we can map the node i to its position j in the cycle, then P0^k(i) is the node at position (j+k) mod m in the cycle.

    # But note: the cycle was built by starting at i and following P0. So the cycle is: 
    #   node0 = i, node1 = P0[i], node2 = P0[P0[i]], etc.
    # Then the node at position j in the cycle is the node we get by applying P0^j to i.

    # Therefore, for a node i at position j in cycle idx, the value after k operations is A[ the node at position (j+k) mod m in the cycle ].

    # But note: the array A is given by the initial values. So we need to know the initial value at the node that is (j+k) mod m steps from i.

    # However, we don't need to store the entire array for each k. We need to find the lexicographically smallest array.

    # We are going to consider the entire array as a function of k.

    # We want to find the minimal k (or the set of k) that minimizes the array.

    # We can consider the following: 

    #   Let F(k) = [ A[P0^k(0)], A[P0^k(1)], ..., A[P0^k(n-1)] ]

    #   We want the lexicographically smallest F(k).

    #   We can try to determine k by checking the first index where the array changes.

    #   But note: the array is determined by the cycles. 

    #   We can break the array into the cycles. The entire array is the concatenation of the cycles (but the indices are fixed).

    #   However, the lexicographic order is by the index order (0 to n-1).

    #   We can consider the following: 

    #       We want to choose k such that the first element is minimized, then the second, etc.

    #   We can use a greedy approach:

    #       Let k0 be the set of k (mod L) that minimize the first element. But L is the lcm of cycle lengths, which is too large.

    #   Instead, we can use the following:

    #       We are allowed to choose any k. The transformation is periodic with period L (the lcm of cycle lengths). 

    #