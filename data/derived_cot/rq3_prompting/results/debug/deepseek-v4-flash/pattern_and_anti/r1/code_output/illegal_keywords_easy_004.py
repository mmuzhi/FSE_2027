from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        nums = sorted(nums, reverse=True)
        seen = set(nums)

        for num in nums:
            if num > 0 and -num in seen:
                return num

        return -1