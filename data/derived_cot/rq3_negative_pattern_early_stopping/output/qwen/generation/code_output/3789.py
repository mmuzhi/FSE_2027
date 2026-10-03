class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        total = n * (n + 1) // 2
        
        # Build a list of b for each a (but we need to index by a)
        # We'll create an array min_b for each starting point l, but we can precompute the minimal b for each a.
        # Actually, we want for each l, the minimal b from edges [a, b] with a >= l.
        # We can precompute an array min_b_from_right, where for each a, we store the minimal b from edges that have a as the smaller number (or from edges with a >= some value).
        # But note: conflictingPairs might not have all a from 1 to n, and a and b are given arbitrarily (but a < b).
        # Let's create an array for each a (from 1 to n) the minimal b that forms a conflicting pair with a (if any). Then, we can do a sweep from right to left to compute the minimal b for each a.

        # First, create an array min_b_for_a of length n+1, initialize with a large number (or infinity) for each a.
        min_b_for_a = [10**9] * (n + 1)
        for a, b in conflictingPairs:
            # We only consider the edge if a < b, but given, so we can use.
            if b < min_b_for_a[a]:
                min_b_for_a[a] = b
        
        # Now, we want for each l (from 1 to n), the minimal b from edges [a, b] with a >= l.
        # We can do a backward sweep: Let min_b_from_right[i] = minimum of min_b_for_a[i], min_b_from_right[i+1], ... up to n.
        min_b_from_right = [10**9] * (n + 2)  # index from 1 to n
        # Initialize with a large number.
        min_b_from_right[n] = 10**9
        for i in range(n - 1, 0, -1):
            min_b_from_right[i] = min(min_b_for_a[i], min_b_from_right[i + 1])
        
        # Now, for each starting index l (from 1 to n), the minimal r that makes the subarray [l, r] invalid is min_b_from_right[l] (if it's not infinity).
        # Then, the number of valid subarrays starting at l is:
        #   If min_b_from_right[l] is 10**9 (no conflicting edge with a >= l), then all subarrays from l to n are valid: n - l + 1.
        #   Else, the valid subarrays are from r = l to min_b_from_right[l] - 1, so min_b_from_right[l] - l.
        # But wait, the condition is: The subarray [l, r] is invalid if r >= min_b_from_right[l] (the minimal b from edges with a >= l). 
        # Actually, the minimal r that makes it invalid is min_b_from_right[l] (because then the edge [a, b] with a >= l and b = min_b_from_right[l] is contained). 
        # So, the valid subarrays starting at l are those with r from l to min_b_from_right[l] - 1, so count = min_b_from_right[l] - l, if min_b_from_right[l] is not infinity.
        # But if there's no edge, then min_b_from_right[l] is 10**9, then the valid subarrays are from l to n, so count = n - l + 1.

        # However, note: The above counts the valid subarrays for a fixed l. But we are going to remove one edge. 

        # But wait, the above method counts the valid subarrays for the entire set of edges (without removal). 

        # Actually, we need to compute for each edge e, the number of valid subarrays after removing e. 

        # But note: The above method (using min_b_from_right) is for the entire set of edges. 

        # We need to compute for each edge e, the effect of removing e. 

        # Alternatively, we can compute the total valid subarrays without any removal (which is the same as the above method) and then for each edge e, compute the additional valid subarrays that are gained by removing e.

        # But note: The condition for validity after removing e is that the subarray must not contain any edge from S' (the original set without e). 

        # The above method (min_b_from_right) uses the minimal b from edges with a