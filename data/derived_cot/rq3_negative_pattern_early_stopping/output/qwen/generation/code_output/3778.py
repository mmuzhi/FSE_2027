class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        transformed = []
        for num in nums:
            if num % 2 == 0:
                transformed.append(0)
            else:
                transformed.append(1)
        transformed.sort()
        return transformed