from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = []
        res = 0
        arr = [float('-inf')] + arr + [float('-inf')]
        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = cur - stack[-1]  # stack[-1] is the previous smaller element
                right = i - cur
                res += arr[cur] * left * right
            stack.append(i)
        return res % (10**9 + 7)