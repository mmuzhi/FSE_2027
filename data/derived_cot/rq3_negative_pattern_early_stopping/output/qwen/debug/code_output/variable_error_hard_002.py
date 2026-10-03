class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        first = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                first[stack.pop()] = i
            stack.append(i)
        
        ans = [-1] * n
        for i in range(n):
            if first[i] != -1 and first[first[i]] != -1:
                ans[i] = nums[first[first[i]]]
        return ans