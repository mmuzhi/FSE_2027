class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        total_subarrays = n * (n + 1) // 2
        # We'll use two pointers and a variable to track the minimal operations for the current window.
        # But we need to count the number of subarrays that require <= k operations.
        # Alternatively, we can use a two-pointer method to count the number of subarrays that can be made non-decreasing with <= k operations.
        # We'll use left and right pointers and a variable to store the current operations and the last value.
        left = 0
        ops = 0
        last = nums[0]
        count = 0
        # We'll traverse with right pointer
        for right in range(n):
            # Update the operations for the current element
            if nums[right] < last:
                ops += (last - nums[right])
            # Update the last value to the maximum of last and nums[right]
            last = max(last, nums[right])
            # Now, if the operations exceed k, we need to move the left pointer