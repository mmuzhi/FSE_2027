class Solution:
    def arrayChange(self, nums: List[int], operations: List[List[int]]) -> List[int]:
        for op in operations:
            old, new = op
            for i in range(len(nums)):
                if nums[i] == old:
                    nums[i] = new
        return nums