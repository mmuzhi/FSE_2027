from typing import List

class Solution:
    def minSubsequence(self, nums: List[int]) -> List[int]:
        total = sum(nums)
        nums.sort(reverse=True)
        sub_sum = 0
        sub_seq = []
        for x in nums:
            sub_sum += x
            sub_seq.append(x)
            if sub_sum > total - sub_sum:
                return sub_seq
        return sub_seq