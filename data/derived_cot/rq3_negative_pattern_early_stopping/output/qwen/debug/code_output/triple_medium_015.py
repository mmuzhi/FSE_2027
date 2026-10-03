class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2
        
        @cache
        def fn(i, x):
            if x < 0 or i == len(toppingCosts):
                return 0
            return min(
                fn(i+1, x),
                toppingCosts[i] + fn(i+1, x - toppingCosts[i]),
                key=lambda y: (abs(y - x), y)
            )
        
        ans = float('inf')
        for bc in baseCosts:
            candidate = bc + fn(0, target - bc)
            if abs(candidate - target) < abs(ans - target) or (abs(candidate - target) == abs(ans - target) and candidate < ans):
                ans = candidate
        return ans