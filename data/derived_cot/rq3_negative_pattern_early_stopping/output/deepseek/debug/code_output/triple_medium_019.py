from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        stack = []
        res = 0
        
        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                count_left = cur - left
                count_right = i - cur
                res += arr[cur] * count_left * count_right
                res %= MOD
            stack.append(i)
        
        while stack:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            count_left = cur - left
            count_right = n - cur
            res += arr[cur] * count_left * count_right
            res %= MOD
        
        return res