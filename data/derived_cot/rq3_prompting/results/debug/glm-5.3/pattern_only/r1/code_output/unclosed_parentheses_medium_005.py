from typing import List

class Solution:
    def validPartition(self, nums: List[int]) -> bool:

        checks = (True, False, nums[0] == nums[1])

        for curr, prev1, prev2 in zip(nums[2:], nums[1:], nums):
            checks = (checks[1], checks[2],
                      (checks[1] and curr == prev1) or                 # condition 1
                      (checks[0] and curr == prev1 == prev2) or        # condition 2
                      (checks[0] and curr == prev1 + 1 == prev2 + 2))  # condition 3

        return checks[2]