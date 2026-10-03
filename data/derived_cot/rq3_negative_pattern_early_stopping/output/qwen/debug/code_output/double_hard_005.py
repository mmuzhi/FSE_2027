class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        
        # First pass: compute first_index (the index of the first greater element for each i)
        stack = []
        first_index = [-1] * n
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                idx = stack.pop()
                first_index[idx] = i
            stack.append(i)
        while stack:
            idx = stack.pop()
            first_index[idx] = -1
        
        # Second pass: compute nge_val (the next greater element value for each index)
        stack = []
        nge_val = [-1] * n
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                idx = stack.pop()
                nge_val[idx] = nums[i]
            stack.append(i)
        
        # Third pass: set ans
        for i in range(n):
            if first_index[i] != -1:
                ans[i] = nge_val[first_index[i]]
        
        return ans
