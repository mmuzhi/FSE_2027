class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        return sorted(list(set(nums)))[-3] if len(list(set(nums))) >= 3 else max(list(set(nums)))