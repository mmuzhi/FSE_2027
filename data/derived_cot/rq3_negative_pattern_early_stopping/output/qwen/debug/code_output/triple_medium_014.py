class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        n = len(arr1)
        expr1_min = float('inf')
        expr1_max = float('-inf')
        expr2_min = float('inf')
        expr2_max = float('-inf')
        expr3_min = float('inf')
        expr3_max = float('-inf')
        expr4_min = float('inf')
        expr4_max = float('-inf')
        
        for i in range(n):
            e1 = i + arr1[i] + arr2[i]
            e2 = i + arr1[i] - arr2[i]
            e3 = i - arr1[i] + arr2[i]
            e4 = i - arr1[i] - arr2[i]
            
            expr1_min = min(expr1_min, e1)
            expr1_max = max(expr1_max, e1)
            expr2_min = min(expr2_min, e2)
            expr2_max = max(expr2_max, e2)
            expr3_min = min(expr3_min, e3)
            expr3_max = max(expr3_max, e3)
            expr4_min = min(expr4_min, e4)
            expr4_max = max(expr4_max, e4)
        
        candidate1 = max(abs(expr1_max), abs(expr1_min))
        candidate2 = max(abs(expr2_max), abs(expr2_min))
        candidate3 = max(abs(expr3_max), abs(expr3_min))
        candidate4 = max(abs(expr4_max), abs(expr4_min))
        
        return max(candidate1, candidate2, candidate3, candidate4)