class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        from functools import cache
        
        @cache
        def fn(i, x):
            if x < 0 or i == len(toppingCosts):
                return 0
            best = fn(i+1, x)
            one_use = toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            best = min(best, one_use, key=lambda y: (abs(y - x), y))
            two_use = toppingCosts[i] * 2 + fn(i+1, x - toppingCosts[i] * 2)
            best = min(best, two_use, key=lambda y: (abs(y - x), y))
            return best
        
        ans = float('inf')
        for bc in baseCosts:
            total = bc + fn(0, target - bc)
            ans = min(ans, total, key=lambda x: (abs(x - target), x))
        return ans