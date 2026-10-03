class Solution:
    def flipgame(self, fronts: List[int], backs: List[int]) -> int:
        bad = set(i for i, j in zip(fronts, backs) if i == j)
        all_nums = set(fronts + backs)
        for num in sorted(all_nums):
            if num not in bad:
                return num
        return 0