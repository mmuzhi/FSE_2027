import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    teams = []
    strengths = []
    index = 1
    for i in range(n):
        t = int(data[index]); b = int(data[index+1]); index += 2
        teams.append(t)
        strengths.append(b)
    
    total = sum(strengths)
    if total % 3 != 0:
        print(-1)
        return
        
    T = total // 3
    
    # We'll use DP: dp[s1][s2] = minimum number of moves (reassignments) to achieve team1 sum s1 and team2 sum s2 (then team3 is total - s1 - s2)
    # But note: we are processing each person. We need to consider the original team of the person.
    # We'll iterate over each person and update the dp table.
    # But the state space is s1 from 0 to total, s2 from 0 to total, which is 1500*1500 = 2.25e6 states, which is acceptable in terms of memory (about 2.25e6 * 4 bytes = 9 MB) but the update for each person (100) would be 100 * 2.25e6 * 3 = 675e6 operations, which is acceptable in C++ but in Python might be slow. But we'll try.

    # We'll use a 2D list for dp, but we can use a dictionary or a 2D array. Since the range is [0, total] for both, we can use a 2D array of size (total+1) x (total+1). But total can be up to 1500, so 1501*1501 = about 2.25e6 elements.

    # Initialize dp: we start with 0 people processed, so s1=0, s2=0, and moves=0.
    # But we can have negative indices? No, we'll use 0 to total.

    # We'll use a 2D array for the current dp state (after processing all people). But we need to update state by state.

    # Alternatively, we can use a DP table that we update for each person. We'll do:

    # dp[i][j] = minimum moves after processing some people, having team1 sum i and team2 sum j.

    # But we need to consider the order. We'll iterate over each person and update the dp table.

    # We'll use a 2D array for the current state, and update it for each person.

    # But note: the same state (i, j) might be reached by different numbers of moves, and we want the minimum moves.

    # We'll initialize dp[0][0] = 0, and all others as a large number.

    # Then for each person, we consider three options: assign to team1, team2, or team3.

    # But note: the person has an original team. If we assign the person to their original team, then no move is needed. Otherwise, one move is needed.

    # However, we are allowed to assign arbitrarily. But the original team is given, so we can precompute for each person the original team.

    # Steps for each person (with strength b and original team t):
    #   For each state (s1, s2) in dp (with value moves_count), we can:
    #       Option 1: assign to team1 -> new_s1 = s1 + b, new_s2 = s2, and if the assigned team (1) is not the original team, then moves_count+1, else moves_count.
    #       Option 2: assign to team2 -> new_s1 = s1, new_s2 = s2 + b, similarly.
    #       Option 3: assign to team3 -> new_s1 = s1, new_s2 = s2, and then the strength is added to team3. But note: we don't track team3 sum, but we can compute it as total - s1 - s2. But we need to check that the new state (s1, s2) is such that s1+b+s2 (if assigned to team3) doesn't exceed the total? Actually, we are tracking the sums of team1 and team2, and the rest is team3. But we must ensure that the assignment is valid: the new state (s1+b, s2) for team1, etc., must not exceed the total? Actually, we are building up the sums, so we can go beyond T? But the target is T