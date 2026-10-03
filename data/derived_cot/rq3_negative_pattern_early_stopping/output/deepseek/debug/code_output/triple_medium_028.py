class Solution:
    def maximumGap(self, nums: list) -> int:
        nums = sorted(nums)
        if len(nums) < 2:
            return 0
        max_gap = 0
        for i in range(len(nums) - 1):
            gap = nums[i+1] - nums[i]
            if gap > max_gap:
                max_gap = gap
        return max_gap