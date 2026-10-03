class Solution:
    def constructTransformedArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        for i in range(n):
            if nums[i] == 0:
                result[i] = 0
            elif nums[i] > 0:
                # Move right by nums[i] steps
                result[i] = (i + nums[i]) % n
            else:
                # Move left by abs(nums[i]) steps
                result[i] = (i - abs(nums[i])) % n
        return result