from typing import List

class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        uniq_non_zero = set()
        for num in nums:
            if num != 0:
                uniq_non_zero.add(num)
        return len(uniq_non_zero)