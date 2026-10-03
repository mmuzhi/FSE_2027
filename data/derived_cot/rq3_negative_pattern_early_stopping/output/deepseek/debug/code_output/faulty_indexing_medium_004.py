from typing import List

class Solution:
    def getLastMoment(self, n: int, left: List[int], right: List[int]) -> int:
        max_left = max(left) if left else 0
        min_right = min(right) if right else n
        return max(max_left, n - min_right)