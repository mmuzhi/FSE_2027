class Solution:
    def validPartition(self, nums: List[int]) -> bool:

        checks = (True, False, nums[0] == nums[1])

        for curr, prev1, prev2 in zip(nums[2:], nums[1:], nums):

            checks  = (checks[1], checks[2],                        # <-- slide the window
                      (checks[1] and curr == prev1) or              # <-- conditiion 1
                      (checks[0] and curr == prev1 == prev2) or     # <-- conditiion 2
                      (checks[0] and curr == prev1 + 1 == prev2 + 2))   

        return checks[2]