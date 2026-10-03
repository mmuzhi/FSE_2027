class Solution:
    def thirdMax(self, nums) -> int:
        distinct_nums = set(nums)
        if len(distinct_nums) < 3:
            return max(distinct_nums)
        else:
            return sorted(distinct_nums)[-3]