class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        left = [-1] * n
        right = [n] * n
        stack = []
        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            if stack:
                left[i] = stack[-1]
            else:
                left[i] = -1
            stack.append(i)
        
        stack = []
        for i in range(n-1, -1, -1):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            if stack:
                right[i] = stack[-1]
            else:
                right[i] = n
            stack.append(i)
        
        res = 0
        for i in range(n):
            res += arr[i] * (i - left[i]) * (right[i] - i)
        
        return res % (10**9 + 7)