from typing import List

class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        n = len(nums)
        mn = min(nums)
        mx = max(nums)
        i = nums.index(mn)
        j = nums.index(mx)

        return min(
            max(i, j) + 1,
            n - min(i, j),
            min(i, j) + 1 + n - max(i, j)
        )