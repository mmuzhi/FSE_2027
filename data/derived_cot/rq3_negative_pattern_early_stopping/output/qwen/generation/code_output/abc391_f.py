import sys
from bisect import bisect_left

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    B = list(map(int, data[2+n:2+2*n]))
    C = list(map(int, data[2+2*n:2+3*n]))
    
    # Precompute the sorted B for binary search
    B_sorted = sorted(B)
    
    # We are going to use binary search on X (the candidate value)
    # The minimum value is at least 3 (since all numbers are at least 1) and maximum is max_A*max_B + max_B*max_C + max_C*max_A
    lo = 1
    hi = 10**18 * 3  # a sufficiently large number, since each term is up to 10^9 * 10^9, so 3e18 is enough

    # But note: the expression is A_i*B_j + B_j*C_k + C_k*A_i, so maximum is max_A * max_B + max_B * max_C + max_C * max_A
    max_val = max(A) * max(B) + max(B) * max(C) + max(C) * max(A)
    hi = max_val

    # We'll define a function F(X) that counts the number of triples (i, j, k) such that A_i*B_j + B_j*C_k + C_k*A_i >= X.
    def F(X):
        count = 0
        # We'll iterate over i and k, but we need to do it efficiently.
        # Instead, we can precompute for each k the value C_k and then for each i, we have A_i.
        # But note: the condition for a fixed (i,k) is:
        #   if X <= C_k * A_i:
        #       count_j = n
        #   else:
        #       threshold = ceil((X - C_k * A_i) / (A_i + C_k))
        #       count_j = n - bisect_left(B_sorted, threshold)
        #
        # However, iterating over i and k (n^2) is too slow (n=200000 -> 40e9 iterations).
        #
        # We need to optimize F(X). Let's try to change the order.
        #
        # We can fix k and then consider all i. Then for each k, we have a fixed C_k.
        # Then for each i, we have A_i and the condition becomes:
        #   if X <= C_k * A_i: then count_j = n
        #   else: threshold = ceil((X - C_k * A_i) / (A_i + C_k))
        #
        # But note: the condition X <= C_k * A_i is equivalent to A_i >= ceil(X / C_k) [if C_k !=0, but C_k>=1]. But we can precompute for each k the value C_k and then for each i, check if A_i >= ceil(X / C_k). But then we need to iterate over i for each k, which is still O(n^2).
        #
        # Alternatively, we can precompute the array of A and then for each k, we can use two parts:
        #   Part 1: i such that A_i >= ceil(X / C_k) -> then count_j = n for these i.
        #   Part 2: i such that A_i < ceil(X / C_k) -> then we need to compute threshold for each i and then count the j's that are >= threshold.
        #
        # But note: the condition for Part 2 is more complicated because the threshold depends on i (via A_i and C_k).
        #
        # Another idea: change the condition. The expression is:
        #   A_i*B_j + B_j*C_k + C_k*A_i >= X
        #   => B_j*(A_i + C_k) >= X - C_k*A_i
        #
        # We can also write:
        #   B_j >= (X - C_k*A_i) / (A_i + C_k)   [if (X - C_k*A_i) > 0]
        #
        # But note: the left side is linear in i for fixed k. We can precompute for each k the array of (A_i + C_k) and (C_k*A_i) for all i.
        #
        # However, we need to count the number of j for each (i,k). We can try to aggregate by k and then by i.
        #
        # Let's try to fix k and then consider the array of A