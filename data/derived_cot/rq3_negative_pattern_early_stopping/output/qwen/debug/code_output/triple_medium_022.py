class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        # We'll try each base cost
        # For each base cost, we want to find the minimal absolute difference between (baseCost + s) and target, where s is the sum of any number of toppings.
        # We can use a BFS for each baseCost to find the minimal absolute difference.

        # But note: the toppingCosts are fixed and we can use each arbitrarily.
        # We'll set a bound for the topping sum: from 0 to target + max(toppingCosts) (or even beyond, but we can set a bound to target + max(toppingCosts) because beyond that the absolute difference will be larger than the current minimal difference)

        # However, we can use a DP for each baseCost separately.

        # But note: the baseCosts can be up to 16, and the toppingCosts up to 16, and target up to 10000, so we can do:

        #   For each baseCost, let x = target - baseCost
        #   If x < 0, then the minimal absolute difference is baseCost - target (but we can also use toppings to reduce the absolute difference? Actually, if baseCost > target, then we can use toppings to reduce the total cost? No, toppings are positive, so we cannot reduce the total cost. So if baseCost > target, then we cannot use toppings to reduce the absolute difference. So the minimal absolute difference is baseCost - target.

        #   But wait, we can use toppings to reduce the total cost? No, toppings are positive, so the total cost is baseCost + s, which is >= baseCost. So if baseCost > target, then the minimal absolute difference is baseCost - target.

        #   However, we can also consider not using any toppings, so the total cost is baseCost, and the absolute difference is |baseCost - target|.

        #   But if baseCost < target, then we can use toppings to get closer.

        #   So for baseCost >= target, the minimal absolute difference is baseCost - target.

        #   For baseCost < target, we can use toppings to get closer.

        #   We can combine: for each baseCost, we want to find the minimal |baseCost + s - target| for s in the set of achievable sums (nonnegative integers that are sums of any number of toppingCosts).

        #   We can use a BFS for each baseCost separately.

        #   But note: the toppingCosts are the same for every baseCost, so we can precompute the set of achievable sums for the toppings? But the bound depends on x = target - baseCost, which varies.

        #   Alternatively, we can precompute all achievable sums up to a bound (say, target + max(toppingCosts)) and then for each baseCost, we look at the achievable sums that are <= target + max(toppingCosts) and then compute the minimal absolute difference.

        #   However, the number of achievable sums might be large, but the bound is target + max(toppingCosts) which is 10000 + 10000 = 20000, and the number of topping types is 16, so we can do a BFS for each baseCost.

        #   But there are up to 16 baseCosts, and for each baseCost we do a BFS with 20000 states, which is 16 * 20000 = 320000 states, which is acceptable.

        #   Steps for fixed baseCost:

        #       x = target - baseCost
        #       If x < 0:
        #           candidate = baseCost
        #           diff = baseCost - target
        #       Else:
        #           We want to find the minimal |s - x| for s in the set of achievable sums (nonnegative integers) that are <= x + max(toppingCosts) (or we can set a bound to x + max(toppingCosts) because beyond that the absolute difference is larger than the current minimal difference)

        #           We'll use a BFS (or DP) to mark all achievable sums up to bound = x + max(toppingCosts)

        #           Let dp = [False]*(bound+1)
        #           dp[0] = True
        #           for c in toppingCosts:
        #               for s in range(bound - c, -1, -1):
        #                   if dp[s]:
        #                       dp[s+c] = True

        #           Then, we find the minimal |s - x| for s in [0, bound] such that