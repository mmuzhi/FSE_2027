class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2
        
        @cache
        def fn(i, x):
            if x < 0 or i == len(toppingCosts):
                return 0
            # Option 1: skip the current topping
            skip = fn(i+1, x)
            # Option 2: take the current topping (at most two times, but the doubling already handled two copies)
            take = toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            # We choose the option (skip or take) that minimizes (absolute difference from x, then the actual value)
            # But note: we are allowed to take the current topping multiple times? Actually, the doubling already gives two copies, so we can take at most two.
            # However, the doubling is done at the beginning, so the list has two copies of each topping. But the recursion goes through the entire doubled list.
            # We are not limited by the number of copies in the recursion because the doubled list has two copies. But note: the doubling is done once, so the list has two copies of each topping. The recursion will consider each topping twice (once for each copy) but that is exactly what we want.
            # Now, we compare the two options. But note: the function returns the total cost of the chosen toppings. We want to choose the one that is closest to x.
            # However, the problem is that we are allowed to choose any number of toppings (with each topping at most two times) and we want the closest to x.
            # But the function `fn` is defined to return the total cost of the chosen toppings. We are comparing two possibilities: skipping or taking the current topping.
            # But note: the function does not consider taking the current topping twice in a row? Actually, the doubled list has two copies, so the current topping (at index i) is one of the two copies. The next copy is at index i+1 (if we are at an even index, then the next is the same topping). But the recursion will consider the next index (i+1) which is the next topping (or the second copy of the same topping). So we are effectively allowing two of the same topping.

            # Now, we need to choose between skip and take. But note: the function returns the total cost. We want to minimize the absolute difference from x.
            # However, the function does not necessarily return the best value for the entire subsequence. We are comparing two possibilities: skipping the current topping or taking it once (since we are at the first copy). But note: the doubled list has two copies, so we can take the same topping again at the next index.

            # Actually, the recursion should consider the entire doubled list. The base case is when we run out of toppings or x becomes negative.

            # But the current recursion only considers one topping at a time. We are allowed to take two of the same topping because the doubled list has two copies. However, the recursion does not force us to take the same topping again. We are free to skip or take.

            # The issue is that the function `fn` is defined to return the total cost of the chosen toppings. We are comparing two possibilities: skipping the current topping or taking it once.

            # However, the problem is that the function does not consider the possibility of taking the current topping twice in a row? Actually, the doubled list has two copies, so the next index (i+1) is the second copy of the same topping. Then we can take it again.

            # But the recursion does not differentiate between the two copies. It just treats them as two separate toppings.

            # Now, the key is to compare the two options (skip and take) and choose the one that is closer to x.

            # However, note: the function `fn` returns the total cost of the chosen toppings. We are trying to get as close as possible to x.

            # But the two options are:
            #   skip: returns the best total cost from the remaining toppings (without the current one) for the remaining x.
            #   take: returns the current topping cost plus the best total cost from the remaining toppings (without the current one) for x - current topping cost.

            # Then we compare these two total costs (skip and take) by their absolute difference from x.

            # However, the current code does:
            #   return min(fn(i+1, x), toppingCosts[i] + fn(i+1, x - toppingCosts[i]), key=lambda y: (abs(y-x), y))

            # But note: the function `fn` is defined to return the total cost of the chosen toppings. The two options are two total costs.