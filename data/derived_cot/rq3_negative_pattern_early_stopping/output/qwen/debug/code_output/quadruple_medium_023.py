from functools import cache

class Solution:
    def closestCost(self, baseCosts: list[int], toppingCosts: list[int], target: int) -> int:
        toppingCosts = toppingCosts * 2
        n = len(toppingCosts)
        
        @cache
        def fn(i, x):
            if i >= n:
                return 0
            if x < 0:
                return 0
            option0 = fn(i+2, x)
            option1 = toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            option2 = 2 * toppingCosts[i] + fn(i+2, x - 2 * toppingCosts[i])
            return min([option0, option1, option2], key=lambda y: (abs(y - x), y))
        
        ans = float('inf')
        for bc in baseCosts:
            total = bc + fn(0, target - bc)
            if abs(total - target) < abs(ans - target) or (abs(total - target) == abs(ans - target) and total < ans):
                ans = total
        return ans