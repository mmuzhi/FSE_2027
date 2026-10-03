class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = [-1]
        res = 0
        n = len(arr)
        
        for i, num in enumerate(arr):
            while len(stack) > 1 and arr[stack[-1]] >= num:
                cur = stack.pop()
                res += arr[cur] * (i - cur) * (cur - stack[-1])
            stack.append(i)
            
        while len(stack) > 1:
            cur = stack.pop()
            res += arr[cur] * (n - cur) * (cur - stack[-1])
            
        return res % (10**9 + 7)