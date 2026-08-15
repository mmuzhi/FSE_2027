from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        unique = sorted(set(nums))
        if len(unique) < 3:
            return unique[-1]
        return unique[-3]