from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        nums.sort(reverse=True)
        for num in nums:
            if num > 0 and -num in s:
                return num
        return -1