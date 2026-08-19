class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        
        s = set(nums)
        for num in sorted(nums, reverse=True):
            if num > 0 and -num in s:
                return num
        return -1