class Solution:
    def minIncrements(self, n: int, cost: List[int]) -> int:
        # We'll create an array `val` to store the minimal increments for each node.
        val = [0] * n
        total_cost = 0
        
        # Traverse from the last node to the first (from leaves to root)
        for i in range(n-1, -1, -1):
            left = 2*i+1
            right = 2*i+2
            if left >= n:
                # Leaf node, no children
                continue
            # For internal node, the minimal value is the sum of the children's minimal values.
            val[i] = val[left] + val[right]
            total_cost += val[i] * cost[i]
        
        return total_cost
