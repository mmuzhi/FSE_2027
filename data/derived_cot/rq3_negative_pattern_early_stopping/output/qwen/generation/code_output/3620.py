class Solution:
    def maxDistinctElements(self, nums: List[int]) = sorted(set(nums))
    if not nums:
        return 0
    nums.sort()
    n = len(nums)
    distinct = 1
    for i in range(1, n):
        if nums[i] - nums[i-1] <= 2*k + 1:
            continue
        else:
            distinct += 1
    return distinct