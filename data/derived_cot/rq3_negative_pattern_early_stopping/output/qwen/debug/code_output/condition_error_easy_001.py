class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        distinct_nums = sorted(set(nums), reverse=True)
        if len(distinct_nums) < 3:
            return distinct_nums[0]
        else:
            return distinct_nums[2]