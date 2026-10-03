class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
        # We'll use dynamic programming. Since the conditions are symmetric, we can consider pairs.
        # But note: the entire row must satisfy both conditions. We can break the problem into two parts: 
        # 1. Adjacent houses must have different colors.
        # 2. Houses at symmetric positions must have different colors.
        #
        # We can use DP with state (i, color) where i is the current house index and color is the color of the current house.
        # But because of the mirror condition, we also need to remember the color of the house at position n-1-i.
        #
        # Alternatively, we can process two houses at a time (a pair) and then combine the results. But the adjacent condition between pairs must be considered.
        #
        # Actually, we can use a DP that goes from left to right and keeps track of the last two houses' colors (to satisfy adjacent conditions) and also the color of the house that is symmetric to the current one (if any). But that might be too heavy.
        #
        # Another idea: since the mirror condition is only about the entire row, we can precompute the constraints and then use a DP that considers the color of the current house and the color of the house that is symmetric to it (if the current house is in the first half). But then, we have to ensure that the color of the current house is different from the house at n-1-i, and also from the adjacent houses.
        #
        # Let's define dp[i][c] as the minimum cost to paint the first i houses (from left) such that the i-th house has color c (0,1,2 representing the three colors). But then, we also need to know the color of the house at position n-1-i. But i and n-1-i might not be the same index until we reach the middle.
        #
        # Alternatively, we can use a DP that goes from left to right and also keeps track of the color of the house that is symmetric to the current one. But that would require storing two colors for each house, which is too much.
        #
        # Another approach: since the mirror condition applies only to the entire row, we can think of the problem as having two independent constraints: the adjacent constraint and the mirror constraint. We can use a DP that considers the color of the current house and the color of the house that is symmetric to it (if we are in the first half). But then, when we reach the middle, we have to ensure that the colors of the two halves are compatible.
        #
        # Actually, we can break the row into two halves: the first n/2 houses and the last n/2 houses. The mirror condition requires that for each i in [0, n/2-1], the color of house i must be different from house n-1-i. Also, adjacent houses must be different.
        #
        # We can use DP for the first half and then combine with the second half. But the second half's colors are determined by the mirror condition, so we can actually just consider the first half and then the second half is fixed by the mirror condition, but we have to ensure that the adjacent condition between the two halves is satisfied.
        #
        # Actually, the problem is symmetric. We can use a DP that goes from left to right and for each house, we remember the color and the color of its mirror (if it exists). But then, the mirror condition is only a constraint for the entire row, so we can enforce it at the end. But that might not be efficient.
        #
        # Let me try a different approach. We can use DP with state (i, c) where i is the current house index (0-indexed) and c is the color of the current house. The recurrence is:
        # dp[i][c] = cost[i][c] + min(dp[i-1][c1] for c1 != c)   [for adjacent condition]
        # But then, we also have the mirror condition: for house i, the color must be different from house n-1-i. So, when we are at house i, we can also check the color of house n-1-i. But we haven't painted house n-1-i yet if we are going from left to right.
        #
        # Alternatively, we can use a DP that goes from left to right and also keeps track of the color of the house that is symmetric to the current one. But that would require storing two colors for each house, which is O(n*3*3) states, which is 9*n, which is acceptable for n=10^5? 9*10^5 is 900,000, which is acceptable in Python