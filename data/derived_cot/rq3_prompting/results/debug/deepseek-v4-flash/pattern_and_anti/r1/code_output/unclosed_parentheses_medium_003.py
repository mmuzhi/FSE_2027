from typing import List

class Solution:
    def flipgame(self, fronts: List[int], backs: List[int]) -> int:
        bad = {i for i, j in zip(fronts, backs) if i == j}
        for i in sorted(set(fronts + backs)):
            if i not in bad:
                return i
        return 0