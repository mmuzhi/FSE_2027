class Solution:
    def maxPathLength(self, coordinates: List[List[int]], k: int) -> int:
        # Separate the k-th point
        k_point = coordinates[k]
        # We'll create two lists: one for points that are less than k_point (for ending path) and one for points that are greater (for starting path)
        # But actually, we need to compute two separate LIS-like sequences: one ending at k_point and one starting from k_point.
        # We can do two separate DP passes: one for the entire set (excluding k_point) for the ending path, and one for the entire set (excluding k_point) for the starting path.
        # But note: the entire set of points is given, and we are allowed to use any subset.

        # We can use coordinate compression and a Fenwick tree or segment tree for 2D, but note that coordinates can be up to 10^9, so we need to compress.

        # Alternatively, we can sort the points and use dynamic programming with a Fenwick tree or segment tree for the second dimension.

        # Steps:
        # 1. For the ending path at k_point:
        #    - Consider all points (x, y) such that x < k_point[0] and y < k_point[1]. We want the longest increasing path (in both x and y) that ends at any of these points, then add 1 for k_point.
        # 2. For the starting path from k_point:
        #    - Consider all points (x, y) such that x > k_point[0] and y > k_point[1]. We want the longest increasing path (in both x and y) that starts at k_point and goes to these points, then add 1 for k_point (but actually, the starting path is the path from k_point to the end, so we just need the longest increasing path starting at k_point, which is 1 + the longest increasing path from the next points).

        # However, note that the entire path must be increasing, so the ending path must be strictly increasing and the starting path must be strictly increasing.

        # We can do:
        #   Let A = all points (x, y) such that x < k_point[0] and y < k_point[1]
        #   Let B = all points (x, y) such that x > k_point[0] and y > k_point[1]

        # Then, the answer is max(1 + (longest increasing path ending at k_point), 1 + (longest increasing path starting at k_point)) but actually, we need to combine both.

        # Actually, the total path is the concatenation of the ending path (from some point to k_point) and the starting path (from k_point to some point). So, the total length is (length of ending path) + (length of starting path) - 1.

        # But note: the ending path and starting path are independent. However, the ending path must end at k_point and the starting path must start at k_point.

        # So, we need to compute:
        #   dp_end = longest increasing path ending at k_point (including k_point)
        #   dp_start = longest increasing path starting at k_point (including k_point)

        # Then, the answer is dp_end + dp_start - 1.

        # But wait, is that always the case? What if the ending path and starting path share points? Actually, the problem states that the path is a list of points from the given coordinates, and each point is distinct. So, the ending path and starting path are disjoint except for k_point.

        # However, the entire path must be increasing, so the ending path must be increasing and the starting path must be increasing, but the entire path is the concatenation, so the last point of the ending path (k_point) must be less than the first point of the starting path (k_point) in both coordinates? Actually, no: the starting path starts at k_point and then goes to points with greater x and y. So, the entire path is increasing.

        # Now, how to compute dp_end and dp_start?

        # For dp_end: We need the longest increasing path (in both x and y) that ends at k_point. This is similar to the longest increasing subsequence in two dimensions. We can do:

        #   Sort all points (from the entire set, but we are only interested in points that are less than k_point) by x (and then by y) and then use dynamic programming with a Fenwick tree or segment tree for the y-coordinate.

        # Similarly for dp_start: sort the points (greater than k_point) by x (and then by y) and then do DP.

        # Steps for dp_end:
        #   Let points_end = [coordinates[i] for