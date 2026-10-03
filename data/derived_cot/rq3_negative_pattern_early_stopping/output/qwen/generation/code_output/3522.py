class Solution:
    def resultsArray(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        res = []
        if k == 1:
            return nums
        for i in range(n - k + 1):
            valid = True
            for j in range(1, k):
                if nums[i+j] != nums[i+j-1] + 1:
                    valid = False
                    break
            if valid:
                res.append(nums[i+k-1])
            else:
                res.append(-1)
        return res