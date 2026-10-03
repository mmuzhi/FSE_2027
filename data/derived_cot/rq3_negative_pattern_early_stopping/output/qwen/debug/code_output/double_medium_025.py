class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return 0
        nums = sorted(nums)
        max_diff = -1
        for i in range(len(nums) - 1):
            gap = nums[i+1] - nums[i]
            if gap > max_diff:
                max_diff = gap
        return max_diff