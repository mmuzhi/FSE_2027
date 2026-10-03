from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = []
        res = 0
        arr = [float('-inf')] + arr + [float('-inf')]
        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                res += arr[cur] * (i - cur) * (cur - left)
            stack.append(i)
        return res % (10**9 + 7)