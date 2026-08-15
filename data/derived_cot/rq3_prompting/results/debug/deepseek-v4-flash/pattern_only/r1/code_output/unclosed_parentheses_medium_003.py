from typing import List

class Solution:
    def flipgame(self, fronts: List[int], backs: List[int]) -> int:
        bad = {f for f, b in zip(fronts, backs) if f == b}
        for x in sorted(set(fronts + backs)):
            if x not in bad:
                return x
        return 0