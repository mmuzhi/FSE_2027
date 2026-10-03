class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        left_bound = [-1] * n
        right_bound = [n] * n
        stack = []
        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            left_bound[i] = stack[-1] if stack else -1
            stack.append(i)
        stack = []
        for i in range(n-1, -1, -1):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            right_bound[i] = stack[-1] if stack else n
            stack.append(i)
        res = 0
        mod = 10**9 + 7
        for i in range(n):
            res = (res + arr[i] * (i - left_bound[i]) * (right_bound[i] - i)) % mod
        return res
