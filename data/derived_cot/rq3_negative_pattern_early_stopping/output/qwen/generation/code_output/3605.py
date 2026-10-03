class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        ans = []
        for num in nums:
            x = -1
            for candidate in range(0, num):
                if candidate | (candidate + 1) == num:
                    x = candidate
                    break
            ans.append(x)
        return ans