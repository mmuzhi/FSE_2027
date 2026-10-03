class Solution:
    def maximumGap(self, nums: list) -> int:
        nums = sorted(nums)
        max_gap = 0
        if len(nums) < 2:
            return 0
        for i in range(len(nums) - 1):
            x = abs(nums[i] - nums[i+1])
            if max_gap < x:
                max_gap = x
        return max_gap