class Solution:
    def maximumAmount(self, coins: List[List[int]]) -> int:
        m = len(coins)
        n = len(coins[0])
        # dp[i][j][k] = maximum coins collected to reach (i, j) with k neutralizations used (k=0,1,2)
        dp = [[[float('-inf')] * 3 for _ in range(n)] for __ in range(m)]
        # Base case: starting cell (0,0)
        # Without neutralizing (0,0)
        if coins[0][0] >= 0:
            dp[0][0][0] = coins[0][0]
        else:
            # For negative, we can choose to neutralize or not, but we can use at most 2 neutralizations.
            # But at start, we can use one neutralization to set it to 0 (if negative) or keep it as is.
            # Actually, if we neutralize (0,0), then we use one neutralization and the value is 0 (since robber is neutralized, so no loss).
            # But note: the problem says the robot starts at (0,0). The starting cell's coin value is given. 
            # The problem doesn't specify if the starting cell is neutralized or not. But we can consider that the robot can neutralize the starting cell if it's negative.
            # However, the ability is to neutralize robbers (negative cells). So, if (0,0) is negative, we can neutralize it, which means no loss (so the robot gains 0 from that cell? Or the cell's effect is avoided, so the robot doesn't gain the negative value, but the starting value is given as coins[0][0]. 
            # Actually, the problem says: "the robot starts at the top-left corner (0,0)" and then moves. So, the starting cell is included. 
            # The example: (0,0) is 0, so no issue. But if (0,0) is negative, then we can neutralize it and set the effect to 0, or not and set to the negative value.
            # But note: the robot starts at (0,0) and then moves. The starting cell is part of the path.
            # So, we have two possibilities for (0,0):
            #   Without neutralization: add coins[0][0] (which is negative)
            #   With neutralization: 0 (if we use one neutralization)
            # But we can use at most two, so we can use one at (0,0) and then one more later.
            # So, we set:
            dp[0][0][0] = coins[0][0]  # without neutralizing
            dp[0][0][1] = 0  # with neutralizing (since negative, neutralization prevents the loss, so effect is 0)
        # But wait, the above base case for negative (0,0) sets two values. But if (0,0) is positive, then only dp[0][0][0] is set.
        # Actually, we need to set for k=0 and k=1 (if negative) and k=0 (if positive). But if positive, then neutralizing doesn't change the value (since the ability is for robbers). So, for positive (0,0), neutralizing (0,0) is not necessary and doesn't change the value. But we can still use a neutralization at (0,0) if we want, but then we are using one neutralization for no benefit. 

        # Actually, the problem says: the robot has a special ability to neutralize robbers in at most 2 cells. So, for positive cells, neutralizing doesn't do anything. So, for positive (0,0), we don't need to set dp[0][0][1] because it's the same as dp[0][0][0]. 

        # But to keep consistency, we can set:
        #   For (0,0):
        #       dp[0][0][0] = coins[0][0]  (without neutralizing)
        #       if coins[0][0] < 0:
        #           dp[0][0][1] = 0  (neutralized, so no effect)
        #       else:
        #           dp[0][0][1] = coins[0][0]  (neutralizing a positive cell does nothing, so same as not neutralizing)

        # But wait, if we neutralize a positive cell, we are using a neutralization without any benefit. So, we can set dp[0][0][1] = coins[0][0] (same as without) but that