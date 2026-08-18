class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        ans = -1
        for x in nums:
            if -x in s and x > ans:
                ans = x
        return ans