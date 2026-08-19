class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        nums = sorted(nums)
        if len(nums) < 2:
            return 0
        res = 0
        for i in range(len(nums) - 1):
            x = abs(nums[i] - nums[i + 1])
            if res < x:
                res = x
        return res