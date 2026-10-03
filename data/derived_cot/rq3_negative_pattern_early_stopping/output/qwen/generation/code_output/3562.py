class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        intervals.sort(key=lambda x: x[1])
        n = len(intervals)
        dp = [[0] * 5 for _ in range(n)]
        best = [0] * 5  # best total weight for 0 to 4 intervals (global)
        res = [0] * 4  # will store the indices for the chosen intervals