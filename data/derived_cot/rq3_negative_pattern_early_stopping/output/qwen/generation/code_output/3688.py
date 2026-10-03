class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        total_sum = sum(nums)
        # Kadane's algorithm for the entire array
        best = -10**18
        current = 0
        for num in nums:
            current = max(0, current + num)
            best = max(best, current)
        # But best might be 0 if all negative, but we need the maximum subarray sum even if negative? 
        # Actually, the problem doesn't say non-negative, so we need to use the standard Kadane's that allows negative.
        # Let me correct Kadane's algorithm for maximum subarray sum (standard version that allows negative)
        best = nums[0]
        current = nums[0]
        for i in range(1, n):
            current = max(nums[i], current + nums[i])
            best = max(best, current)
        
        # Now, we need to consider removing each distinct value
        # But we cannot do for each distinct value by iterating over the array because it's too slow.
        # Alternative approach: 
        # We can use a two-pass to get the maximum subarray sum for the entire array, and then for each distinct value, 
        # we can compute the maximum subarray sum of the array without that value by using a segment tree or something, but that's complex.
        # Another idea: 
        # We can use the fact that the array without x is the original array with x's removed. 
        # The maximum subarray sum without x is the maximum of the maximum subarray sums of the segments (the parts between x's).
        # But we need to compute that efficiently.
        #
        # However, note that the problem constraints are up to 10^5, so we need an O(n) or O(n log n) solution.
        #
        # Let me try to use a different approach: 
        # We can compute the maximum subarray sum for the entire array (best) and also the total sum (total_sum). 
        # But that doesn't help directly.
        #
        # Another idea: 
        # We can use a dictionary to store the positions of each distinct value. Then, for each distinct value, we can split the array into segments and compute the maximum subarray sum for each segment using Kadane's. But that is O(n^2) in worst-case.
        #
        # But wait, there is a known efficient method: 
        # We can use a segment tree or a sparse table to answer range maximum subarray queries, but that is complex.
        #
        # Alternatively, we can use a divide and conquer method to compute the maximum subarray sum for the entire array, and then for each distinct value, we can compute the maximum subarray sum without that value by excluding the segments that contain that value. 
        #
        # But I think the intended solution is to use the following observation: 
        # The maximum subarray sum after removing x is the maximum of:
        #   - The maximum subarray sum that ends before the first occurrence of x
        #   - The maximum subarray sum that starts after the last occurrence of x
        #   - The maximum subarray sum that is entirely between two occurrences of x
        #
        # But then, we need to know the positions of x. 
        #
        # However, we can precompute the positions for each distinct value. Then, for each distinct value, we can compute the maximum subarray sum for the segments. 
        #
        # But the total work is O(n^2) in the worst-case (if there are many distinct values and each has many occurrences). 
        #
        # But note: the distinct values are the ones that appear in the array. The worst-case is when all elements are distinct, then we have n distinct values. For each distinct value, the array is split into two segments (if the value appears once) or more. The total work is O(n^2) which is 10^10 for n=10^5, which is not feasible in Python.
        #
        # We need a better approach.
        #
        # Let me think: 
        # The maximum subarray sum of the array without x is the maximum of the maximum subarray sums of the segments (the parts between x's). 
        # But note: the entire array without x is the same as the original array with x's removed. 
        #
        # We can use a two-pointer to compute the maximum subarray sum for the entire array, and then for each distinct value, we can use a two-pointer to compute the maximum subarray sum that doesn't include any x. But that is O(n) per distinct value, which is O(n^2) overall.
        #
        # But wait, there is a known