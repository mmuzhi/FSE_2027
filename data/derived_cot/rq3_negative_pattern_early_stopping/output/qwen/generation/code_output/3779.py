class Solution:
    def maxWeight(self, pizzas: List[int]) = sorted(pizzas)
    n = len(pizzas)
    k = n // 4  # number of days
    odd_days = (k + 1) // 2
    even_days = k // 2

    # We need to assign the largest pizzas to be the maximums of odd-day groups and the next largest to be the second maximums of even-day groups.

    # But note: each group has four pizzas. So we need to form groups such that the odd-day groups have the largest four pizzas (each group's maximum is one of the largest), and even-day groups have the next largest.

    # Actually, we can think greedily: 

    # The total gain is the sum of the maximums of the odd-day groups and the second maximums of the even-day groups.

    # We have to use all pizzas.

    # The optimal strategy is to assign the largest 4 * odd_days pizzas to be the maximums of the odd-day groups and the largest 4 * even_days pizzas to be the maximums of the even-day groups? Not exactly.

    # Actually, we can form the groups by taking the entire sorted array and then:

    # For odd days, we want the largest available pizza to be the maximum of that group. For even days, we want the next largest available pizza (after the ones used in odd days) to be the second maximum of that group.

    # But wait, we can interleave. 

    # Let me consider: 

    # We have to form k groups. Each group has four pizzas. 

    # The total gain is the sum of the maximums of the odd-indexed groups (1st, 3rd, etc.) and the second maximums of the even-indexed groups (2nd, 4th, etc.).

    # We can form the groups arbitrarily. 

    # The optimal way is to assign the largest pizzas to be the maximums of the odd-day groups and the next largest to be the second maximums of the even-day groups, but we have to form groups of four.

    # Actually, we can do:

    # Sort the array in descending order.

    # Then, we can assign the largest 4 * odd_days pizzas to be the maximums of the odd-day groups. But then, for each odd-day group, we need three more pizzas. Similarly, for even-day groups, we need four pizzas, but we want the second maximum to be as large as possible.

    # Alternatively, we can consider: 

    # The total gain is the sum of the largest odd_days * 1 (for the maximums) and the next largest even_days * 2 (for the second maximums). But we have to use all pizzas.

    # Actually, we can use a greedy grouping:

    # Sort the array in descending order.

    # Then, the first 4 * odd_days pizzas will be the maximums of the odd-day groups. But then, for each odd-day group, we need three more pizzas. Similarly, the next 4 * even_days pizzas will be the maximums of the even-day groups, but then we need three more for each even-day group.

    # But wait, that doesn't work because the groups must be disjoint.

    # Another idea: 

    # We need to assign each pizza to a "role": 
    # - Some pizzas will be the maximum of an odd-day group.
    # - Some pizzas will be the second maximum of an even-day group.
    # - The remaining pizzas will be the rest.

    # But the rest are the third and fourth in the groups.

    # Actually, the total gain is the sum of the maximums of the odd-day groups and the second maximums of the even-day groups.

    # We can choose which pizzas are the maximums for odd days and which are the second maximums for even days.

    # The maximums for odd days should be the largest pizzas. The second maximums for even days should be the next largest pizzas.

    # But note: a pizza can only be used once.

    # So, the optimal strategy is:

    # 1. Sort the array in descending order.
    # 2. The largest odd_days * 1 pizzas will be the maximums for the odd-day groups.
    # 3. The next even_days * 1 pizzas will be the second maximums for the even-day groups.
    # 4. The remaining pizzas will be the third and fourth in the groups.

    # But then, how do we form the groups? 

    # Actually, we can form the groups by taking the largest 4 * odd_days + 4 * even_days = n pizzas. 

    # Then, for each odd-day group, we take one maximum (from the first odd_days * 1) and then three from the remaining (