class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = []
        res = 0
        
        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = cur - stack[-1] if stack else cur + 1
                right = i - cur
                res += arr[cur] * left * right
            stack.append(i)
            
        while stack:
            cur = stack.pop()
            left = cur - stack[-1] if stack else cur + 1
            right = len(arr) - cur
            res += arr[cur] * left * right
            
        return res % (10**9 + 7)