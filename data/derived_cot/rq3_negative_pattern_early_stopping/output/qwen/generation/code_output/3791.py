class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        # We'll create an array to mark used baskets, but that would be too slow.
        # Instead, we can use a pointer for each basket and then use a greedy approach with a min-heap for available baskets.
        # But note: we need to consider the original order (leftmost available). 
        # Alternatively, we can sort the baskets by capacity, but then we lose the original index. 
        # We need to know the original index to determine leftmost.

        # Another idea: 
        # We can iterate over baskets and record the available baskets (with their index) that have capacity >= current fruit's requirement.
        # But we need to assign the leftmost available basket for each fruit.

        # We can use a pointer for each basket and then use a two-pointer technique? Not exactly.

        # Let's try this: 
        # We'll keep an array "used" of length n (baskets) to mark if a basket is used.
        # But that would be O(n^2) in worst-case.

        # We need a better approach.

        # We can use a greedy algorithm with a pointer for the current basket index and a min-heap for baskets that are available and have capacity >= current fruit's requirement.

        # Steps:
        # 1. We'll iterate over fruits (from left to right).
        # 2. For each fruit, we want to find the smallest index basket (from the beginning) that is available and has capacity >= fruit.
        # 3. We can precompute the baskets and then use a pointer to track the next available basket? But then we need to check capacity.

        # Alternatively, we can use a segment tree or a Fenwick tree? But that might be overkill.

        # Another idea: 
        # Sort the baskets by capacity, but then we lose the original index. But we can store the index with the capacity.

        # Actually, we can do the following:
        # - We'll create an array of baskets with (capacity, index).
        # - Then, we want to assign to each fruit the smallest index basket (from the original order) that is available and has capacity >= fruit.

        # We can use a greedy matching with a pointer for each basket and a priority queue for baskets that are available and have capacity >= current fruit.

        # Steps:
        # 1. Create an array of baskets with (capacity, index).
        # 2. Sort the baskets by capacity (ascending) and then by index (ascending) if capacities are equal? Actually, we need to consider the original index for leftmost.
        # 3. But then, we need to assign the smallest index basket that is available and has capacity >= fruit.

        # Alternatively, we can use a two-pointer approach if we sort the fruits and baskets by capacity, but then we have to map back to the original index.

        # Let me think differently:
        # We want to assign each fruit to the leftmost available basket with capacity >= fruit. 
        # We can process the baskets in order (original order) and then for each basket, if it is not used, then we can use it for the next fruit that requires capacity <= basket's capacity and hasn't been assigned yet.

        # But we need to assign fruits in order.

        # Another idea: 
        # We can use a greedy algorithm that goes through the baskets and for each basket, if it is not used, then we can "reserve" it for the next fruit that requires capacity <= basket's capacity and hasn't been assigned. But we need to assign the leftmost available basket for each fruit.

        # We can use a pointer for the current basket index (from 0 to n-1) and then for each fruit, we look for the smallest index basket (from 0 to current) that is available and has capacity >= fruit. But then we have to mark it as used.

        # But worst-case, this is O(n^2).

        # We need a more efficient method.

        # Let me consider using a min-heap for the baskets that are available. But we need to know the original index to determine leftmost.

        # Actually, we can do the following:
        # 1. We'll keep an array "used" of booleans for baskets, initially all False.
        # 2. We'll iterate over fruits (from left to right).
        # 3. For each fruit, we'll iterate over baskets from left to right (using an index pointer) until we find an available basket with capacity >= fruit. Then we mark that basket as used and count it as placed.
        # 4. But worst-case, if many baskets are used, then for each fruit we might have to scan almost all baskets. Worst-case O(n^2) which is