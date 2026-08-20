class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        
        s = set(nums)
        ans = -1
        for i in range(len(nums)):
            if nums[i] > 0 and -nums[i] in s:
                ans = max(ans, nums[i])
        return ans