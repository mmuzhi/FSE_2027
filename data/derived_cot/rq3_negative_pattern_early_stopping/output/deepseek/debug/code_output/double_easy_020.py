class Solution:
    def thirdMax(self, nums) -> int:
        distinct = list(set(nums))
        if len(distinct) < 3:
            return max(distinct)
        else:
            return sorted(distinct)[-3]