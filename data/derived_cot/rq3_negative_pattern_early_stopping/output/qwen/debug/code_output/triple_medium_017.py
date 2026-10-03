class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        val1 = []
        val2 = []
        val3 = []
        val4 = []
        for i in range(len(arr1)):
            val1.append(i + arr1[i] + arr2[i])
            val2.append(i + arr1[i] - arr2[i])
            val3.append(i - arr1[i] + arr2[i])
            val4.append(i - arr1[i] - arr2[i])
        all_vals = val1 + val2 + val3 + val4
        if not all_vals:
            return 0
        max_val = max(all_vals)
        min_val = min(all_vals)
        return max(max_val, -min_val)
