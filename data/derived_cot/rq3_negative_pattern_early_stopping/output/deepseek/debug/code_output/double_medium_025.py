from typing import List

class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        nums = sorted(nums)
        max_gap = 0
        if len(nums) < 2:
            return 0
        for i in range(len(nums) - 1):
            x = abs(nums[i] - nums[i+1])
            if x > max_gap:
                max_gap = x
        return max_gap