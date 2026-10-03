import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    B = [int(next(it)) for _ in range(n)]
    k = int(next(it))
    queries = []
    for _ in range(k):
        x = int(next(it)); y = int(next(it))
        queries.append((x, y))
        
    # We'll compress the values of A and B together
    all_vals = sorted(set(A + B))
    comp_map = {}
    for idx, val in enumerate(all_vals):
        comp_map[val] = idx+1  # 1-indexed for Fenwick tree
    
    # We need to compute for each query (x, y): 
    #   sum_{i=0}^{x-1} sum_{j=0}^{y-1} |A[i] - B[j]|
    #
    # We can use the following trick:
    #   Let F(x, y) = sum_{i=0}^{x-1} sum_{j=0}^{y-1} |A[i] - B[j]|
    #   = sum_{j=0}^{y-1} [ sum_{i=0}^{x-1} |A[i] - B[j]| ]
    #
    # For a fixed B[j], let v = B[j]
    #   S(v, x) = sum_{i=0}^{x-1} |A[i] - v|
    #   = (number of A[i] (i< x) <= v) * v - (sum of A[i] (i< x) <= v) + (sum of A[i] (i< x) > v) - (number of A[i] (i< x) > v) * v
    #
    # So if we can quickly, for a given v and given x, compute:
    #   count_le = number of i in [0, x-1] with A[i] <= v
    #   sum_le = sum of A[i] for i in [0, x-1] with A[i] <= v
    #   count_gt = x - count_le
    #   sum_gt = (prefix_sum_A[x-1] - sum_le)   [if we have prefix_sum_A for the first x elements]
    #
    # But note: the first x elements of A are not sorted, so we cannot use a simple sorted array for A.
    #
    # We can precompute a Fenwick tree for A (by index) but then the condition is by value.
    #
    # Alternatively, we can precompute a Fenwick tree for the entire A (all n elements) and then for a given x, we consider only the first x elements. 
    # But then we need to update the Fenwick tree as x increases.
    #
    # We can do offline queries for A: sort the queries by x.
    #
    # Steps:
    #   1. Compress the values of A and B.
    #   2. Build a Fenwick tree for the entire A (all n elements) for frequency and for sum.
    #   3. But then the query is for the first x elements (by index) and for a given value v.
    #
    # However, the first x elements are not the entire A, so we cannot use a single Fenwick tree for the entire A.
    #
    # We can use a segment tree that is built over the indices of A (from 0 to n-1) and then query the range [0, x-1] for values <= v.
    #
    # But then we need to build a 2D structure (index and value) which is complex.
    #
    # Another idea: Use Mo's algorithm? Not likely.
    #
    # Given the complexity, I decide to use a different approach:
    #
    #   Precompute two arrays for B: 
    #       Let's build a Fenwick tree for the entire B (all n elements) for frequency and sum, but then the query is for the first y elements (by index) and for a given value v.
    #
    #   But then the query for a fixed B[j] (which is a value) and for the first x elements of A is not directly related.
    #
    # Let's swap the summation order:
    #   F(x, y) = sum_{i=0}^{x-1} sum_{j=0}^{y-1} |A[i] - B[j]|
    #            = sum_{j=0}^{