class Solution:
    def isZeroArray(self, nums: List[int], queries: List[List[int]]) -> bool:
        n = len(nums)
        diff = [0] * (n + 1)
        for l, r in queries:
            diff[l] += 1
            if r + 1 < n:
                diff[r + 1] -= 1
        
        cover = [0] * n
        cover[0] = diff[0]
        for i in range(1, n):
            cover[i] = cover[i - 1] + diff[i]
        
        for i in range(n):
            if cover[i] < nums[i]:
                return False
        return True