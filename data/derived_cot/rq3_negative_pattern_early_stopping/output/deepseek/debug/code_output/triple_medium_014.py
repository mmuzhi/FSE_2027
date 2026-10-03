from typing import List

class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        val1, val2, val3, val4 = [], [], [], []
        for i in range(len(arr1)):
            val1.append(i + arr1[i] + arr2[i])
            val2.append(i + arr1[i] - arr2[i])
            val3.append(i - arr1[i] + arr2[i])
            val4.append(i - arr1[i] - arr2[i])
        ans = 0
        ans = max(ans, max(val1) - min(val1))
        ans = max(ans, max(val2) - min(val2))
        ans = max(ans, max(val3) - min(val3))
        ans = max(ans, max(val4) - min(val4))
        return ans