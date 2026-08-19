class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        distinct = list(set(nums))
        return max(distinct) if len(distinct) < 3 else sorted(distinct)[-3]