import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    xs = [int(next(it)) for _ in range(n)]
    ps = [int(next(it)) for _ in range(n)]
    q = int(next(it))
    queries = []
    for _ in range(q):
        L = int(next(it)); R = int(next(it))
        queries.append((L, R))
    
    # Create sorted list of all unique coordinates for compression (only xs are needed for the tree, but queries use L and R)
    # We'll compress the xs only, but for queries we need to map L and R to the compressed indices.
    sorted_x = sorted(set(xs))
    # But note: the villages are given in sorted order, so we can use the sorted_x to map each x to an index.
    # However, we need to handle queries that might have L and R not in sorted_x.

    # We'll create a mapping from coordinate to index for the xs, but for queries we need to find the first index >= L and last index <= R.

    # Alternatively, we can use bisect to find the range in xs for the query [L, R].
    # Steps for a query (L, R):
    #   left_index = first index in xs such that xs[index] >= L
    #   right_index = last index in xs such that xs[index] <= R
    # Then the villages from left_index to right_index (inclusive) are in [L, R].

    # But note: the villages are given in sorted order, so we can use bisect_left and bisect_right.

    # However, we can also build a Fenwick tree (Binary Indexed Tree) for the compressed xs.

    # Let's compress the xs and then build a Fenwick tree for the population array.

    # Step 1: Compress xs and build an array for the Fenwick tree.
    # We'll map each x to an index from 1 to n (for Fenwick tree, which uses 1-indexing).

    # But note: the queries might ask for coordinates that are not in xs, so we need to find the boundaries.

    # We'll do:
    #   sorted_x = sorted(set(xs))   # This is the sorted unique coordinates of villages.
    #   Then, for a given L, we find the first index in sorted_x that is >= L, which is the starting point.
    #   Similarly, for R, the last index in sorted_x that is <= R.

    # Then, the villages in [L, R] are from the index 'left_index' to 'right_index' in the original list? Not exactly.

    # Actually, the villages are given in sorted order by x, so the i-th village in the original list is at xs[i] and has ps[i].

    # But note: the xs are distinct and sorted, so the mapping from x to the village is one-to-one.

    # We can create an array for the Fenwick tree that is of length n, and the index in the Fenwick tree corresponds to the position in sorted_x.

    # However, we don't need to compress the entire coordinate space, only the xs. And we can use the sorted_x to map the query boundaries.

    # Steps:
    #   Let sorted_x be the sorted list of xs (which is already sorted, but we take unique? Actually, the input says distinct and increasing, so no duplicates).
    #   Then, for a query (L, R):
    #       left_bound = bisect.bisect_left(sorted_x, L)
    #       right_bound = bisect.bisect_right(sorted_x, R) - 1
    #   But note: bisect_right returns the insertion position, so the last index that is <= R is bisect_right(sorted_x, R) - 1.

    #   Then, if left_bound > right_bound, the answer is 0.
    #   Otherwise, we need to sum the populations from the village at sorted_x[left_bound] to sorted_x[right_bound].

    # But note: the villages are given in increasing order, but the population array ps is given in the order of increasing x.

    # However, we can build a Fenwick tree (or segment tree) for the array of populations, but the indices in the Fenwick tree are the positions in sorted_x.

    # But wait: the villages are given in sorted order by x, so the i-th village in the original list is the i-th in sorted_x. So we can use the index in sorted_x to index the population.

    # However, the array of populations is given in the order of increasing x, so we can create an array "arr" of length n, where:
    #   arr[i] = population of the village at sorted_x[i