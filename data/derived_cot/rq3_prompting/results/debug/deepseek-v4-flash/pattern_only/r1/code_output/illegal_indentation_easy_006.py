from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        uniq = sorted(set(nums))
        return uniq[-3] if len(uniq) >= 3 else uniq[-1]