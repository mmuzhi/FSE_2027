class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        s1 = 0
        arr = []
        for i in range(n):
            left = nums[i] * i - s1
            s2 = total - s1 - nums[i]
            right = s2 - nums[i] * (n - 1 - i)
            arr.append(left + right)
            s1 = s1 + nums[i]
        return arr