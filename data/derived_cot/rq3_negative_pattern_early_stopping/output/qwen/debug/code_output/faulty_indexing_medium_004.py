class Solution:
    def getLastMoment(self, n: int, left: List[int], right: List[int]) -> int:
        if not left and not right:
            return 0
        time_left = max(left) if left else 0
        time_right = n - min(right) if right else n
        return max(time_left, time_right)