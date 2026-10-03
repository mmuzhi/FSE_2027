class Solution:
    def maximumGap(self, nums: list) -> int:
        nums = sorted(nums)
        max_gap = float('-inf')
        if len(nums) < 2:
            return 0
        for i in range(len(nums)-1):
            gap = nums[i+1] - nums[i]
            if max_gap < gap:
                max_gap = gap
        return max_gap