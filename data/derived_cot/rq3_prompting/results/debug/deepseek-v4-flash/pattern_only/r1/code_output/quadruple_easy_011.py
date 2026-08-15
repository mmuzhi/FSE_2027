from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        seen = set(nums)
        ans = -1
        for num in nums:
            if num > 0 and -num in seen:
                ans = max(ans, num)
        return ans