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
                res = (res + arr[cur] * (cur - left) * (i - cur)) % MOD
            stack.append(i)
        
        while stack:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            res = (res + arr[cur] * (cur - left) * (n - cur)) % MOD
        
        return res