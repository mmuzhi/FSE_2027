import bisect

class Solution:
    def solveQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        # Build dictionary: value -> sorted list of indices
        val_to_indices = {}
        for idx, val in enumerate(nums):
            if val not in val_to_indices:
                val_to_indices[val] = []
            val_to_indices[val].append(idx)
        
        # For each value, sort the list of indices
        for val in val_to_indices:
            val_to_indices[val].sort()
        
        # Prepare the answer for each query
        ans = []
        for q in queries:
            val = nums[q]
            if val not in val_to_indices:
                ans.append(-1)
                continue
            L = val_to_indices[val]
            pos = bisect.bisect_left(L, q)
            # The query index q is at position pos in L
            # Now, consider the left and right neighbors
            res = float('inf')
            # Check left neighbor (if exists)
            if pos > 0:
                left_val = L[pos-1]
                # Calculate circular distance from q to left_val
                d = min(abs(q - left_val), n - abs(q - left_val))
                if d < res:
                    res = d
            # Check right neighbor (if exists)
            if pos < len(L) - 1:
                right_val = L[pos+1]
                d = min(abs(q - right_val), n - abs(q - right_val))
                if d < res:
                    res = d
            if res == float('inf'):
                ans.append(-1)
            else:
                ans.append(res)
        return ans