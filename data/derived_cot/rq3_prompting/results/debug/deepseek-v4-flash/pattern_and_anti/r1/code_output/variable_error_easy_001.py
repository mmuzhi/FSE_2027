from typing import List

class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        def dnc(l, r, lo, hi):
            if l >= r:
                return -1
            if l == r - 1:
                return l if lo == hi else -1

            mid = (l + r) // 2
            left = sum(nums[l:mid])
            right = sum(nums[mid:r])

            left_ind = dnc(l, mid, lo, hi + right)
            if left_ind != -1:
                return left_ind
            return dnc(mid, r, lo + left, hi)

        return dnc(0, len(nums), 0, 0)