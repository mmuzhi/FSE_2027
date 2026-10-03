class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        # Double the toppingCosts to simulate two uses
        toppingCosts = toppingCosts * 2
        
        # Use memoization to avoid recalculating the same state
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def fn(i, x):
            # Base case: if we've processed all toppings or x is negative, return 0
            if i == len(toppingCosts) or x < 0:
                return 0
            # We have two choices: skip the current topping or take it
            # But note: we can take the current topping and then consider the next topping (not skipping two)
            # However, we want to consider using the same topping twice, but we have two copies so we can use each topping twice.
            # The doubling of the list allows us to use each topping twice, but the DFS must consider each topping independently.
            # We don't skip two, we just consider the next index.
            # But wait, the original code did skip two. Let me explain: the original code intended to use each topping at most once by doubling and then skipping the next one. But that doesn't allow two uses.
            # Actually, the doubling is to allow two uses, but the DFS must be able to use a topping twice. However, the DFS above (with skip two) does not allow two uses of the same topping because after using one, we skip the next one (which is the second copy). 
            # So we need to change the DFS to not skip two. But then we would use the same topping multiple times without limit. 
            # Alternatively, we can use a different DFS that doesn't double the list and uses a state that tracks the index and the remaining uses for each topping. But that is complex.
            #
            # Let's change the DFS to not skip two. We'll consider each topping independently and allow multiple uses. But then we must limit the uses to two. However, we doubled the list so that we have two copies. Then we can use each topping at most twice by having two copies. But the DFS must consider each topping in the doubled list as a separate topping and allow using each one once. 
            #
            # Actually, the doubling is a common trick to allow two uses. Then we can use a DFS that doesn't skip two, but just goes to the next index. But then we would use each topping (in the doubled list) only once. And that is exactly what we want: two uses per original topping.
            #
            # So we change the DFS to:
            #   Option 1: skip the current topping -> fn(i+1, x)
            #   Option 2: take the current topping -> toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            #
            # But note: the original code did `i+2` to skip the next one. We change that to `i+1`.
            #
            # However, the original code had a bug in the base case and the recursion. Let's fix the base case and change the recursion to `i+1`.
            #
            # But wait, the original code had:
            #   return min(fn(i+1, x), toppingCosts[i] + fn(i+2, x-toppingCosts[i]), key=lambda y: (abs(y-x), y))
            #
            # We change it to:
            #   return min(fn(i+1, x), toppingCosts[i] + fn(i+1, x - toppingCosts[i]), key=lambda y: (abs(y-x), y))
            #
            # However, note that the function `fn` is defined to return the sum of the subsequence of toppings that is closest to `x`. But the base case returns 0, which is the sum of an empty subsequence. Then we compare the absolute difference from `x` and the actual sum.
            #
            # But the problem: the function `fn` is called with `x` being the remaining value to achieve. We want to get a total topping cost that is as close as possible to `x`.
            #
            # Let's fix the DFS to use `i+1` and remove the colon in the base case.
            #
            # However, note: the original code had a syntax error: `if x < 0 or i == len(toppingCosts): return 0` -> the colon was missing in the condition? Actually, the code had a colon but the condition was written with a colon and then a return. But the code snippet provided had a colon in the condition, so I think it was a typo in the problem statement.
            #
            # Let's rewrite the DFS correctly.
            #