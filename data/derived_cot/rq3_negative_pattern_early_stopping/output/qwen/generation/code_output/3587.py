class Solution:
    def maxScore(self, n: int, k: int, stayScore: List[List[int]], travelScore: List[List[int]]) -> int:
        # We'll use dynamic programming.
        # dp[i][j] = maximum total points after i days (i from 0 to k) ending in city j.
        # Base case: day0 (i=0) - we can start in any city, but we have to choose an action for day0.
        # However, note that on day0, we don't have a previous city. But the problem says we can choose any city as starting point.
        # But then, for day0, we can either stay (if we start in city j, then we get stayScore[0][j]) or move (but moving from a city to another on day0: but we started in j, so moving from j to some other city? Actually, the problem doesn't specify that we must have a previous city for day0. But the travelScore is defined for all cities, including the starting one.

        # Actually, the problem says: "they can choose any city as their starting point", and then each day they choose an action. So for day0, we are in the starting city. Then, we choose to stay or move.

        # We can consider day0 separately.

        # Alternatively, we can think of the journey as having k days, and we are free to choose the starting city. Then, for each day, we are in a city and choose an action.

        # Let dp[i][j] be the maximum points after i days (i from 0 to k) and ending in city j.

        # For day0 (i=0), we can start in any city j. Then, we can either stay or move. But wait, if we start in city j, then for day0, we are in city j. Then, we can choose to stay (then we get stayScore[0][j]) or move (then we get travelScore[j][l] for some l, and then we are in l at the end of day0). 

        # But note: the problem says the journey consists of exactly k days. So we have k days, and we are free to choose the starting city. 

        # Actually, the problem does not specify that the starting city is fixed. So we can choose the starting city arbitrarily. Then, for day0, we are in that city. Then, we choose an action for day0.

        # However, the problem says: "they can choose any city as their starting point", meaning that the starting city is chosen at the beginning, and then the journey (k days) begins.

        # So, for day0, we are in the starting city. Then, we choose to stay or move. 

        # We can use DP with state (day, city). 

        # Steps:
        # 1. Initialize dp[0][j] for each city j. But how? We can start in any city, so we can set dp[0][j] to the maximum between:
        #    a) Staying in j on day0: stayScore[0][j]
        #    b) Moving from some other city to j on day0? But wait, we start in j, so we haven't moved from anywhere. 

        # Actually, for day0, we are in city j. Then, we can either stay (then we get stayScore[0][j]) or move (then we get travelScore[j][l] for some l, but then we are in l at the end of day0). 

        # But wait, the problem says: "each day, the tourist has two choices". So for day0, we are in city j (the starting city). Then, we choose to stay or move. 

        # So, for day0, if we start in j, then:
        #   Option1: stay -> points = stayScore[0][j]
        #   Option2: move -> points = travelScore[j][l] for some l (and then we are in l at the end of day0). 

        # But note: the travel action on day0: we are leaving city j and going to city l. Then, we are in city l at the end of day0. 

        # So, we can set dp[0][j] to the maximum points we can have at the end of day0 if we started in j and then chose an action.

        # But then, how do we account for the starting city? We can choose any starting city. 

        # Actually, we can consider that the journey has k days, and we are free to choose the starting city. Then, for day0, we are in the starting city. Then, we choose an action. 

        # We can