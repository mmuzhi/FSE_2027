from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        unique = sorted(set(nums), reverse=True)
        return unique[2] if len(unique) >= 3 else unique[0]