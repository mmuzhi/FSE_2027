import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); q = int(next(it))
    A = [0] + [int(next(it)) for _ in range(n)]
    B = [0] + [int(next(it)) for _ in range(n)]
    
    # Precompute the positions for each value in A and B
    posA = defaultdict(list)
    posB = defaultdict(list)
    for i in range(1, n+1):
        posA[A[i]].append(i)
        posB[B[i]].append(i)
    
    # We'll store the queries
    queries = []
    for i in range(q):
        l = int(next(it)); r = int(next(it)); L = int(next(it)); R = int(next(it))
        queries.append((l, r, L, R))
    
    # We'll use a function to compute the frequency of a value x in a segment [l, r] for array A or B
    def count_in_segment(positions, l, r, x):
        # If x is not in the dictionary, then count 0
        if x not in positions:
            return 0
        arr = positions[x]
        # Find the first index >= l
        left_index = bisect.bisect_left(arr, l)
        # Find the first index > r
        right_index = bisect.bisect_right(arr, r)
        return right_index - left_index
    
    # But note: the entire array A and B are of length n, and the indices are from 1 to n.
    # However, the query indices are given as 1-indexed and inclusive.

    # But wait: the problem says the arrays are given as A_1, A_2, ... A_N, and the query indices are 1-indexed.

    # We'll process each query by checking for each distinct value that appears in either segment? 
    # But we cannot iterate over all values from 1 to n because n=200000 and q=200000.

    # Instead, we can use a different idea: we know that the condition is that the multiset of A[l:r+1] equals the multiset of B[L:R+1].
    # We can use a dictionary to store the frequency of each value in the A segment and B segment, but we don't know which values to check.

    # Alternatively, we can use a two-pointer style for the entire array and use a frequency array for the current A segment and B segment, but then we have to update for each query.

    # But note: the queries are independent. We cannot share state between queries.

    # We need to check for all values from 1 to n? That is too slow.

    # Another idea: we can use a hashing technique for the frequency vector. But the frequency vector is of length up to n (values from 1 to n) and we cannot store a vector of length n for each query.

    # Alternatively, we can use a rolling hash for the frequency vector. But the frequency vector is sparse.

    # We can use a dictionary for the current query for A and B, but then we have to reset for each query.

    # But the worst-case length of the segments is 200000, and the distinct values in a segment might be up to 200000, and then we do 200000*log(occurrence) per query, which is about 200000*18 = 3.6e6 per query, and 200000 queries would be 720e9 operations — too slow.

    # We need to optimize.

    # Let's change our approach: precompute the entire frequency arrays for A and B for the whole array, and then use prefix sums for each value.

    # We can precompute for each value x (from 1 to n) the prefix sum array for A and B.

    # But the memory is O(n^2) which is too big.

    # Another idea: use Mo's algorithm but the queries must be processed in order.

    # Or use offline queries? But the problem says "in order".

    # Alternatively, we can use a persistent segment tree? But that is too complex.

    # Let's think: we need to check for each value x, the frequency in A[l:r] equals that in B[L:R]. 

    # We can precompute for each value x the list of positions in A and B, and then for a query, we can use binary search to count the frequency of x in A[l:r] and B[L:R]. 

    # Then, we can iterate over the distinct values that appear