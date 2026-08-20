class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        distinct = sorted(set(nums))
        return distinct[-3] if len(distinct) >= 3 else distinct[-1]