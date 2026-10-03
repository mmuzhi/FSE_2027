class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        res = float('inf')
        for i in range(0, n - k + 1):
            res = min(res, nums[i+k] - nums[i])
        return res
