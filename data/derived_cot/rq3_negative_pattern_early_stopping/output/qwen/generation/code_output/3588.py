class Solution:
    def countWinningSequences(self, s: str) -> int:
        n = len(s)
        mod = 10**9 + 7
        
        # dp[i][last][diff] = number of ways after i rounds, with last move being 'last' (0,1,2) and score difference (Bob - Alice) = diff
        # We'll use a dictionary or a 3D array. But n is 1000, and diff can be from -1000 to 1000 (so 2001 states). 
        # We can use a 2D DP for the current round and update for the next round.
        # Alternatively, we can use a dictionary for the state (last, diff) and update for each round.
        # But the state space is 3 * 2001 = 6003 states per round, and 1000 rounds, so 6e6 states, which is acceptable in C++ but in Python might be borderline in speed, but we can try with memoization and iterative DP.

        # Alternatively, we can use a 2D DP array for the current round: dp[last][diff] for the current round.
        # But the diff can be negative, so we need to offset.

        # Let's define the offset: the maximum negative diff is -n, maximum positive is n, so total range is 2*n+1. But n=1000, so 2001 states.

        # We'll use a dictionary for the current round's states to save memory and time, but 6003 states per round is acceptable.

        # Alternatively, we can use a 2D array of size 3 x (2*n+1). But 3 * 2001 * 1000 is 6e6 integers, which is acceptable in C++ but in Python might use a lot of memory (about 6e6 * 4 bytes = 24 MB, which is acceptable).

        # But we can use a dictionary to avoid iterating over all possible diff values (many will be 0). But the range is fixed.

        # Let's use a 2D DP array for the current round: dp[last][diff_index] where diff_index is from 0 to 2000, representing diff from -1000 to 1000.

        # But we need to map the actual diff (which can be negative) to an index. Let base = 1000, then diff_index = diff + 1000.

        # Steps:
        # 1. Initialize dp[last][diff_index] for the first round.
        # 2. For each round, update the next state.

        # But note: the constraint for Bob's consecutive moves: he cannot choose the same as the previous. So, for round i (i>=1), the previous move is known.

        # We'll do:
        # dp[i][last][diff] = number of ways to reach state (last, diff) after i rounds.

        # But we can do iterative DP (round by round) and use a 2D array for the current round.

        # Let dp[last][diff] be the state after processing the current round (i). We'll update for the next round.

        # However, the state space is 3 * 2001, which is 6003 states. We can use a 2D list of zeros of size 3 x 2001 for each round.

        # But 1000 rounds * 6003 states is 6e6 states, which is acceptable in Python if we do it in a bottom-up way.

        # Alternatively, we can use memoization and recursion with caching, but iterative DP is better for such problems.

        # Steps for iterative DP:

        # 1. Initialize dp[last][diff] for the first round (i=0). 
        #    For the first round, Bob can choose any of the 3 moves. 
        #    For each move, we calculate the outcome (if Bob wins, then diff = 1; if Alice wins, then diff = -1; if tie, diff = 0).
        #    But note: the first round, no previous move, so no constraint on consecutive same.

        # 2. Then, for each round from 1 to n-1 (0-indexed, so round 1 to n-1), update the dp for the next round.

        # But wait, the rounds are from 0 to n-1. We have n rounds.

        # Actually, we can index rounds from 0 to n-1.

        # Let dp be a 2D array (3 x