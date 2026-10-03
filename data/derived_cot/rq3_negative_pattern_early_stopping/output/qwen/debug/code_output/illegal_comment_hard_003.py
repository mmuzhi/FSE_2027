class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        first_greater = [-1] * n
        first_greater_index = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                idx = stack.pop()
                first_greater[idx] = nums[i]
                first_greater_index[idx] = i
            stack.append(i)
        
        next_greater2 = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                idx = stack.pop()
                next_greater2[idx] = nums[i]
            stack.append(i)
        
        ans = [-1] * n
        for i in range(n):
            if first_greater[i] != -1:
                ans[i] = next_greater2[first_greater_index[i]]
        return ans