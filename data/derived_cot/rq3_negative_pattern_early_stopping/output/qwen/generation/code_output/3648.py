class Solution:
    def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
        n = len(fruits)
        # If n == 1, then only one room, but n>=2 per constraints
        # We'll create a 3D DP? Or maybe use a different approach.
        # Alternatively, note that the three children's paths are independent and the grid is large.
        # But note: the problem is symmetric and the meeting point is (n-1, n-1). 
        # Another idea: the three children's paths can be seen as three "diagonals" or lines that cover the grid.
        # Actually, we can consider that the grid can be divided into three parts, but the fruits are collected only once per room.
        # We can use a greedy approach: assign each room to the child that can reach it with the least "cost" or something, but that might not work because the paths are constrained.

        # Alternatively, we can use the fact that the three children must meet at (n-1, n-1) and their paths are monotonic in certain ways.

        # Observation: The three children's paths are constrained such that:
        #   A: from (0,0) to (n-1, n-1) with steps (1,0), (0,1), (1,1)
        #   B: from (0, n-1) to (n-1, n-1) with steps (1,-1), (1,0), (1,1)
        #   C: from (n-1, 0) to (n-1, n-1) with steps (-1,1), (0,1), (1,1)

        # But note: the grid is n x n. The total number of rooms is n*n.

        # However, note that the three children together must cover the entire grid? Not necessarily, but we want to maximize the sum.

        # Another idea: the problem is equivalent to covering the grid with three paths (each from their start to (n-1, n-1)) and the union of the rooms is the set of collected fruits.

        # But the grid is large (up to 1e6 cells) and the paths are constrained. We need an efficient solution.

        # Let me think of the grid as having three "diagonals" or layers. Actually, note that the three children's paths are similar to the three "directions" from the three corners.

        # Actually, we can consider that the grid can be partitioned into three sets of rooms, each set being the rooms that are "controlled" by one child. But note, a room can be controlled by multiple children.

        # But the problem is that the paths are constrained by the moves, so not every room can be reached by every child.

        # Let me define for each room (i, j) the minimal steps required for each child to reach it:

        # For child A: steps_A(i, j) = max(i, j)
        # For child B: steps_B(i, j) = max(i, n-1-j)
        # For child C: steps_C(i, j) = max(n-1-i, j)

        # But note: the children must take exactly n-1 steps to reach (n-1, n-1). So a room (i, j) is reachable by child A if steps_A(i, j) <= n-1, and similarly for others.

        # However, the problem is that the three children's paths are independent, and we want to maximize the sum of fruits in the union of the rooms they visit.

        # This is a set cover problem with three sets, but the sets are constrained by the paths and the grid is large.

        # Alternatively, we can use a DP that considers the three children's positions and the steps taken, but that would be O(n^3) which is 1e9 for n=1000 — too slow.

        # Another idea: the grid is n x n, and the three children's paths are from their corners to (n-1, n-1). The meeting point is (n-1, n-1). 

        # Consider that the three children's paths can be seen as three lines that start from their corners and end at (n-1, n-1). The grid can be divided into three regions:

        #   Region A: rooms that are on the "A" path or can be reached by A without being blocked by B or C? Not exactly.

        # Actually, note that the three children's paths must be chosen such that they are "compatible" in the sense that they don't conflict too much. But the problem is that we can choose any path for each child as long as the moves are allowed.

        #