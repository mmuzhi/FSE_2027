import sys
from bisect import bisect_right, bisect_left

class Fenw:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)

    def update(self, index, value):
        # index is 1-indexed in Fenw, but our compressed array is 0-indexed, so we use index+1?
        # Actually, we'll build the Fenw tree for the compressed coordinates (0-indexed) but internally we use 1-indexed.
        i = index + 1
        while i <= self.n:
            if value > self.tree[i]:
                self.tree[i] = value
            i += i & -i

    def query(self, index):
        # query prefix [0, index] (0-indexed)
        res = 0
        i = index + 1
        while i:
            if self.tree[i] > res:
                res = self.tree[i]
            i -= i & -i
        return res

    def range_query(self, l, r):
        # query [l, r] (0-indexed) for maximum
        if l > r:
            return 0
        res = 0
        i = r + 1
        while i:
            if self.tree[i] > res:
                res = self.tree[i]
            i -= i & -i
        l += 1
        i = l
        while i <= r:
            if self.tree[i] > res:
                res = self.tree[i]
            i += i & -i
        return res

    # Alternatively, we can use a segment tree for range maximum query, but Fenw tree is easier for point update and prefix maximum.

    # But note: we want to update a point and then query the maximum in [0, X_i] (which is a prefix). So we can use a Fenw tree that stores the maximum in the prefix.

    # However, the update is: we set the value at a point to the maximum of the current value and the new value.

    # But the query is for the entire prefix [0, index] (which is the maximum value in the tree from 0 to index).

    # The above query function does that.

    # But note: the Fenw tree for maximum doesn't support arbitrary range maximum queries as easily as for sums. We can do prefix maximum, but not arbitrary range.

    # Actually, we want to query the maximum in [0, X_i] (which is the entire prefix up to X_i). So we can use the prefix query.

    # But note: our compressed coordinates are sorted, and we want to query all values <= X_i. In the compressed array, we map X_i to an index, and then query [0, index] (where index is the compressed index of X_i).

    # However, the update is for the value A[i] (which is a number) and we map it to a compressed index.

    # But note: the dp update: we want to update the value at the compressed index of A[i] to the new length.

    # Then, the query for a given X_i: we get the compressed index of X_i, and then query the prefix maximum from 0 to that index.

    # But note: the dp update is: we want to set the value at the compressed index of A[i] to the maximum between the current value and (max_{w < A[i]} dp[w] + 1).

    # How to get max_{w < A[i]} dp[w]? We can use the Fenw tree to query the prefix maximum for the compressed index of A[i]-1 (but note: the values are integers, but we have compressed, so we need to find the largest value that is less than A[i]).

    # Actually, we can do:

    #   Let pos = bisect_left(compressed, A[i])   # the first index in compressed that is >= A[i]
    #   Then, the values less than A[i] are in [0, pos-1].

    #   Then, we query the Fenw tree for the prefix [0, pos-1] to get the maximum dp value for values less than A[i].

    #   Then, new_length = query_result + 1

    #   Then, update the Fenw tree at pos with new_length.

    # But note: the Fenw tree we built is for the compressed coordinates (0-indexed) and we update the tree at the compressed index of A[i] (which is pos) with new_length.

    # However, the Fenw tree we built above is for prefix maximum. But note: the Fenw tree for maximum does not support arbitrary range maximum, but we are only doing prefix queries (from 0 to index). So