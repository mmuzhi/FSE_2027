from typing import List

class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left_sum = 0
        for i in range(len(nums)):
            # The left part is from 0 to i-1, so the right part is from i+1 to end.
            # The condition is left_sum == (total - left_sum - nums[i]) - nums[i] + nums[i] ... no.
            # The condition is: left_sum == (total - left_sum - nums[i])
            if left_sum == total - left_sum - nums[i]:
                return i
            left_sum += nums[i]
        return -1