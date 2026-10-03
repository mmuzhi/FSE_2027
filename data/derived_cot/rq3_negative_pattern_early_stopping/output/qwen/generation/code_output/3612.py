class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        # We'll check for each starting index i from 0 to n - 2*k (inclusive)
        # For each i, check if the subarray starting at i is strictly increasing and the subarray starting at i+k is strictly increasing.
        for i in range(n - 2*k + 1):
            # Check subarray starting at i
            if all(nums[j] < nums[j+1] for j in range(i, i+k-1)):
                # Check subarray starting at i+k
                if all(nums[j] < nums[j+1] for j in range(i+k, i+2*k-1)):
                    return True
        return False