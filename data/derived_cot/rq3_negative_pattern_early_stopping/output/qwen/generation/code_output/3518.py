class Solution:
    def maxScore(self, a: List[int], b: List[int]) -> int:
        dp_prev = [0] + [-10**18] * 4
        for num in b:
            for k in range(4, 0, -1):
                if dp_prev[k-1] != -10**18:
                    candidate = dp_prev[k-1] + a[k-1] * num
                    if candidate > dp_prev[k]:
                        dp_prev[k] = candidate
        return dp_prev[4]