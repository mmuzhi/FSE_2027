class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2
        
        @cache
        def fn(i, x):
            if i >= len(toppingCosts):
                return 0
            # We can choose to skip the current topping or take one or two of the current topping?
            # But note: the list is duplicated so we can take two of the same topping consecutively without skipping?
            # Actually, the problem allows at most two of each topping. Since we duplicated the list, we can use two of the same topping by taking two consecutive ones.
            # However, the recursion should consider: 
            #   Option 1: skip the current topping (i+1)
            #   Option 2: take one of the current topping (i+1) and then we can take another one at the same index? But we are at index i, and the next index is i+1 which is the same topping (because we duplicated). So we can take two in a row without skipping.
            # But the original code tried to use `i+2` to skip the next one, which is not correct because we want to allow two of the same topping consecutively.
            # Let's change the recursion to allow taking one or two of the current topping without skipping the next one (which is the same topping). But note: the list is duplicated, so we have two copies of each topping. We can use two of the same topping by taking two consecutive ones. However, we cannot use more than two. So we can take 0, 1, or 2 of the current topping.

            # Actually, the problem says "at most two of each topping", and we duplicated the list so that we have two copies. Then we can use a DP that goes through the list and for each topping we can take 0, 1, or 2. But note: the duplicated list means that we have two identical toppings. We can use two of them by taking two consecutive ones.

            # However, the original code's recursion was:
            #   min(fn(i+2, x), toppingCosts[i] + fn(i+1, x - toppingCosts[i]), ...)
            # This does not allow taking two of the same topping because it skips the next one. Instead, we should allow:
            #   Option 1: skip the current topping (i+1)
            #   Option 2: take one of the current topping (i+1) and then we can take another one at the same index? But we are at index i, and the next index is i+1 which is the same topping. So we can take two by doing: toppingCosts[i] + toppingCosts[i] + fn(i+1, x - 2*toppingCosts[i])
            # But wait, the problem does not require to use the duplicated list in this way. Alternatively, we can use a different approach.

            # Let me reframe: We have two copies of each topping. We can use 0, 1, or 2 of each. We can use a DP that iterates over the toppings and for each topping we can take 0, 1, or 2. But note: the list is duplicated, so we can use two of the same topping by taking two consecutive ones without skipping.

            # Actually, the intended solution might be to use a two-pointer or a DP that goes through the list and for each topping we can take 0, 1, or 2. But the recursion in the original code was trying to use two of the same topping by having two copies and then skipping the next one? That doesn't seem right.

            # Let's change the recursion to allow taking 0, 1, or 2 of the current topping without skipping the next one (which is the same topping). But note: the list is duplicated, so we have two copies. We can use two of the same topping by taking two consecutive ones. However, we cannot use more than two. So we can take 0, 1, or 2 of the current topping.

            # But the recursion should be:

            #   Option 1: skip the current topping -> fn(i+1, x)
            #   Option 2: take one of the current topping -> toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            #   Option 3: take two of the current topping -> 2 * toppingCosts[i] + fn(i+1, x - 2 * toppingCosts[i])

            # However, note that the list is duplicated, so we have two copies. But we are allowed to use two of the same topping, so we don't need to skip the next one. We can use two of