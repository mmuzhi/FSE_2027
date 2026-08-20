class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = []
        res = 0
        arr = arr + [0]  # sentinel to flush remaining elements from the stack

        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                res += arr[cur] * (i - cur) * (cur - left)
            stack.append(i)
        return res % (10**9 + 7)