class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2
        
        @cache
        def fn(i, x):
            if x < 0 or i == len(toppingCosts):
                return 0
            take = toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            skip = fn(i+1, x)
            take_val = take
            skip_val = skip
            if abs(take_val - x) < abs(skip_val - x) or (abs(take_val - x) == abs(skip_val - x) and take_val < skip_val):
                return take_val
            else:
                return skip_val
        
        ans = float('inf')
        for bc in baseCosts:
            res = fn(0, target - bc)
            total = bc + res
            if abs(total - target) < abs(ans - target) or (abs(total - target) == abs(ans - target) and total < ans):
                ans = total
        return ans