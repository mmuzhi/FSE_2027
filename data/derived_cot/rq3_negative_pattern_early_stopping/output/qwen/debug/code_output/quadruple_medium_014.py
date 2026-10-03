class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts = toppingCosts * 2
        
        @cache
        def fn(i, x):
            if i == len(toppingCosts) or x <= 0:
                return 0
            # We have two choices: skip the current topping or take one (the second copy will be considered in the next state)
            take = fn(i+1, x - toppingCosts[i]) + toppingCosts[i]
            skip = fn(i+1, x)
            # We choose the one that is closer to x, but if the same absolute difference, choose the smaller cost (or the one that is closer in the usual sense, but the problem says: closestCost, so we compare by absolute difference and then by the actual cost if tie)
            # But note: the function returns the total cost of toppings chosen. We are trying to minimize the absolute difference from x (which is the remaining target for this base cost).
            # However, the function returns the sum of the chosen toppings. We are comparing the total cost (base + toppings) to the target.
            # But in the recursion, we are only concerned with the topping part. The base part is fixed for this call.
            # We want to choose the option that is closer to x (the remaining target). But note: the function returns the sum of the toppings chosen, and we are comparing to x (the remaining target). However, the two options are:
            #   take: total topping cost = take, which is the sum of the chosen toppings including the current one.
            #   skip: total topping cost = skip.
            # But wait, the function returns the sum of the chosen toppings. We are comparing the topping sum to x (the remaining target). However, the function is defined to return the sum of the subsequence of toppingCosts[i:] that is closest to x. But note: the function does not necessarily return the maximum sum <= x. It returns the sum that is closest to x.

            # The original code used: min(fn(i+2, x), toppingCosts[i] + fn(i+1, x-toppingCosts[i]), key=lambda y: (abs(y-x), y))
            # But that was incorrect because it skipped two items.

            # Now, we have two choices: skip and take. But note: the two copies are independent. We can take one or two? Actually, the doubling method allows two uses, so we can take two by taking two separate items. But the recursion above only takes one. However, the next state (i+1) will consider the next item (which is the second copy) and we can take that one too. So the two copies are handled naturally.

            # But wait, the function `fn` is defined to consider the entire subsequence from i to the end. So if we take the first copy, then the second copy is still available and we can take it in the next state. So the two copies are independent.

            # However, the original code intended to use two copies by having a doubled list and then stepping by 1. So we should change the recursion to:

            #   take = fn(i+1, x - toppingCosts[i]) + toppingCosts[i]
            #   skip = fn(i+1, x)

            # But note: the state (i+1, x) and (i+1, x - toppingCosts[i]) are independent.

            # Now, we choose between take and skip. But note: the function is supposed to return the sum of the chosen toppings that is closest to x. However, the two options are not necessarily the best because we might have more than two choices? Actually, the doubling method is to have two copies, so we can use two of the same topping. The recursion above does not explicitly allow two uses because we are only taking one copy at a time. But the two copies are consecutive and we are allowed to take the second copy in the next state.

            # However, the problem is that the function `fn` is defined to consider the entire subsequence from i to the end. So if we take the first copy, then the second copy is still available and we can take it in the next state. So the two copies are independent and the recursion will naturally allow two uses.

            # But wait, the function `fn` is defined to return the sum of the chosen toppings that is closest to x. The two options are:

            #   Option 1: skip the current topping -> then the best from the rest is skip.
            #   Option 2: take the current topping -> then the best from the rest is take.

            # However, we are allowed to take the current topping twice? No, because the doubled list has two copies. We can