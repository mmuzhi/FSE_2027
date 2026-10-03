class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left_sum = 0
        for i in range(len(nums)):
            # At index i, the left_sum is the sum of elements from 0 to i-1.
            # The right_sum is the total minus the left_sum and the current element.
            right_sum = total - left_sum - nums[i]
            if left_sum == right_sum:
                return i
            left_sum += nums[i]
        return -1