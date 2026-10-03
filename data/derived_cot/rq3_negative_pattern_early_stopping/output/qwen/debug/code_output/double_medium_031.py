from typing import List

class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        n = len(arr1)
        if n == 0:
            return 0
        
        expr1 = []
        expr2 = []
        expr3 = []
        expr4 = []
        
        for i in range(n):
            expr1.append(i + arr1[i] + arr2[i])
            expr2.append(i + arr1[i] - arr2[i])
            expr3.append(i - arr1[i] + arr2[i])
            expr4.append(i - arr1[i] - arr2[i])
        
        candidates = []
        for expr in [expr1, expr2, expr3, expr4]:
            max_val = max(expr)
            min_val = min(expr)
            candidates.append(max(max_val, -min_val))
        
        return max(candidates)