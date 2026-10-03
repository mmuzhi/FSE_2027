class Solution:
    def minCost(self, nums: List[int]) -> int:
        n = len(nums)
        dp = {}
        
        def dfs(l, r):
            if r - l + 1 <= 2:
                return max(nums[l:r+1])
            if (l, r) in dp:
                return dp[(l, r)]
            res = float('inf')
            # Option 1: remove two from the first three
            for i in range(l, l+3):
                if i >= r:
                    continue
                # We remove two elements: one at i and one other from the first three
                # But we need to choose two from the first three (l, l+1, l+2)
                # So, we can remove i and another j from the first three (j != i)
                # But actually, we can choose any two from the first three, so we can remove two indices from [l, l+2]
                # But we must remove two, so we need to choose two indices from the first three.
                # Let's consider removing two indices: i and j, where j is another index from [l, l+2] and j != i.
                # Then, the next state will be from i+1 to r, but actually, the array is contiguous, so we remove two elements and the next state is the segment from the next index after the last removed to r? Actually, no: the array is the remaining elements, so we remove two elements, and the next state is the segment from the next index after the last removed to r, but we must skip the removed indices.

                # Actually, the operation removes two elements from the first three, so the next state is the segment from the next index after the last removed to r. But the removed indices are two, so the next state starts from the next index after the maximum index of the two removed.

                # But we are allowed to choose any two from the first three, so we can remove two indices from [l, l+2]. Then, the next state is from the next index after the last removed to r.

                # But we must consider that the two removed indices are not necessarily adjacent. So, the next state's left index is the next index after the maximum of the two removed indices.

                # However, we can also consider that the operation removes two elements, so the next state is the segment from the next index after the two removed to the end.

                # But we are using a segment (l, r). So, if we remove two indices, say i and j (with i < j), then the next state is from j+1 to r.

                # But we are iterating over one of the two to remove. Actually, we need to choose two indices from the first three. So, we can do:

                # Let's consider removing two indices: we choose two indices from [l, l+2]. Then, the next state is from the next index after the second removed index (the maximum of the two) to r.

                # But we are iterating over one index i. Then, we need to choose another index j from the first three (l, l+1, l+2) that is not i.

                # Actually, we can precompute the two indices we remove. So, we can do:

                # For each pair (i, j) where i and j are distinct indices in [l, l+2] and i < j, then the next state is from j+1 to r.

                # Then, the cost for this operation is max(nums[i], nums[j]), and then we add the cost of the next state.

                # But we are iterating over i from l to l+2, and then for each i, we consider the other two indices in [l, l+2] (excluding i) as j.

                # Alternatively, we can iterate over all pairs in [l, l+2] and then the next state is from max(i, j)+1 to r.

                # But we are already iterating over i from l to l+2. So, for each i, we can consider the other two indices.

                # Let me restructure: we are going to consider all pairs (i, j) from the first three (l, l+1, l+2) with i < j. Then, the next state is from j+1 to r.

                # Then, the cost is max(nums[i], nums[j]) + dfs(j+1, r)

                # But we are iterating i from l to l+2, so we can do:

                # Actually, we can do:

                # for i in range(l, l+3):
                #   for j in range(i+1, min(l+3, r+1)):
                #       if j > r: continue
                #       Then